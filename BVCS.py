import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Configuration
VIDEO_FOLDER = r"C:\path\to\videos"
OUTPUT_FOLDER = r"C:\path\to\output_sheets"
THUMBNAILS = 8
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"  # Replace with your system font path if necessary
REFERENCE_WIDTH = 2560
REFERENCE_HEIGHT = 1440
FONT_SIZE = 75  
TEXT_AREA_HEIGHT = 400  
THUMBNAIL_PADDING = 10  

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_video_metadata(video_path):
    command = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=width,height', '-of', 'default=noprint_wrappers=1', video_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    metadata = {}
    for line in result.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=')
            metadata[key.strip()] = value.strip()
    return metadata

def format_duration(duration):
    duration = float(duration)
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    formatted = []
    if hours > 0:
        formatted.append(f"{hours}h")
    if minutes > 0:
        formatted.append(f"{minutes}m")
    if seconds > 0 or not formatted:
        formatted.append(f"{seconds}s")
    return ' '.join(formatted)

def extract_thumbnails(video_path, output_dir, num_thumbnails):
    duration = float(get_video_metadata(video_path).get('duration', 0))
    if duration < num_thumbnails:
        num_thumbnails = max(1, int(duration))  
        print(f"Video too short for {THUMBNAILS} thumbnails. Adjusting to {num_thumbnails}.")
    
    interval = max(duration / num_thumbnails, 1)
    thumbnails = []
    for i in range(num_thumbnails):
        timestamp = min(int(interval * i), int(duration) - 1)
        output_file = os.path.join(output_dir, f'thumb_{i + 1}.jpg')
        command = [
            'ffmpeg', '-ss', str(timestamp), '-i', video_path,
            '-frames:v', '1', '-q:v', '2', output_file
        ]
        try:
            result = subprocess.run(command, capture_output=True, timeout=10)
            if os.path.exists(output_file):
                thumbnails.append(output_file)
            else:
                print(f"Warning: Thumbnail {i + 1} failed to generate at timestamp {timestamp}s.")
        except subprocess.TimeoutExpired:
            print(f"Timeout: Thumbnail {i + 1} at {timestamp}s took too long.")
            continue
    
    while len(thumbnails) < THUMBNAILS:
        if thumbnails:
            thumbnails.append(thumbnails[-1])
        else:
            break
    
    return thumbnails

def create_contact_sheet(video_path, metadata, thumbnails):
    rows = 2
    cols = 4
    sheet_width = REFERENCE_WIDTH
    sheet_height = REFERENCE_HEIGHT
    thumbnail_y_offset = TEXT_AREA_HEIGHT + THUMBNAIL_PADDING
    available_height = sheet_height - thumbnail_y_offset - (THUMBNAIL_PADDING * (rows + 1))
    available_width = sheet_width - (THUMBNAIL_PADDING * (cols + 1))

    scaled_thumb_width = available_width // cols
    scaled_thumb_height = available_height // rows
    aspect_ratio = int(metadata.get('width', 16)) / int(metadata.get('height', 9))
    if aspect_ratio > 1:
        scaled_thumb_height = int(scaled_thumb_width / aspect_ratio)
    elif aspect_ratio < 1:
        scaled_thumb_width = int(scaled_thumb_height * aspect_ratio)
    
    contact_sheet = Image.new('RGB', (sheet_width, sheet_height), color='black')
    draw = ImageDraw.Draw(contact_sheet)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    text_lines = [
        f"Name: {os.path.basename(video_path)}",
        f"Duration: {format_duration(metadata.get('duration'))}",
        f"Resolution: {metadata.get('width')}x{metadata.get('height')}"
    ]
    y_offset = 20
    for line in text_lines:
        draw.text((20, y_offset), line, fill='white', font=font)
        y_offset += FONT_SIZE + 20  
    
    for i in range(rows * cols):
        x = (i % cols) * (scaled_thumb_width + THUMBNAIL_PADDING) + THUMBNAIL_PADDING
        y = (i // cols) * (scaled_thumb_height + THUMBNAIL_PADDING) + thumbnail_y_offset
        if i < len(thumbnails):
            img = Image.open(thumbnails[i]).resize((scaled_thumb_width, scaled_thumb_height))
            contact_sheet.paste(img, (x, y))
    
    output_path = os.path.join(OUTPUT_FOLDER, os.path.basename(video_path) + '_sheet.jpg')
    contact_sheet.save(output_path)
    print(f"Contact sheet saved: {output_path}")

def batch_process():
    for video_file in os.listdir(VIDEO_FOLDER):
        if video_file.endswith(('.mov', '.avi', '.mp4', '.hap', '.hapq', '.dxv')):
            video_path = os.path.join(VIDEO_FOLDER, video_file)
            temp_thumb_dir = os.path.join(OUTPUT_FOLDER, 'temp', os.path.splitext(video_file)[0])
            os.makedirs(temp_thumb_dir, exist_ok=True)
            
            metadata = get_video_metadata(video_path)
            thumbnails = extract_thumbnails(video_path, temp_thumb_dir, THUMBNAILS)
            create_contact_sheet(video_path, metadata, thumbnails)
            
            for thumb in set(thumbnails):
                if os.path.exists(thumb):
                    os.remove(thumb)
            os.rmdir(temp_thumb_dir)

if __name__ == '__main__':
    batch_process()
#Made by Noah Montez 2025
#https://github.com/montezma