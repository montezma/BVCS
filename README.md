# BVCS
Batch Video Contact Sheet maker

A Python script for generating video contact sheets with metadata and thumbnail previews for video files. It supports formats such as .mov, .avi, .mp4, .hap, .hapq, and .dxv. Each contact sheet includes:

File Name

Duration: Formatted as hours, minutes, and seconds.

Resolution: Video dimensions (e.g., 1920x1080, 4K). Supports square and standard res

Thumbnails: 8 evenly spaced frames extracted from the video.

The output is a high-quality image (.jpg) suitable for previews, archives, or sharing.

--------------------------------------------------------------------------------------------------

**Features**

Supports Multiple Video Formats: .mov, .avi, .mp4, .hap, .hapq, .dxv

Dynamic Thumbnail Adjustment: Adjusts thumbnail extraction for short videos.

Text Metadata Overlay: File name, duration, and resolution displayed.

Customizable Layout: Resolution and text font sizes can be adjusted.

Error Handling: Handles timeouts, missing frames, and invalid video files.

--------------------------------------------------------------------------------------------------

 **Requirements**

Python 3.8+

ffmpeg (Installed and added to PATH)

ffprobe (Part of FFmpeg)

Python Libraries:

Pillow

Install dependencies via pip:

pip install pillow ffmpeg-python

--------------------------------------------------------------------------------------------------

 Folder Structure

Video Contact Sheet Maker/
├── script.py       # Main Python script
├── output_sheets/  # Folder for generated contact sheets
├── temp/           # Temporary folder for thumbnails
└── Videos/         # Source folder for video files

--------------------------------------------------------------------------------------------------

 **Configuration**

Update the following variables in script.py to suit your needs:

VIDEO_FOLDER = r"C:\path\to\videos"
OUTPUT_FOLDER = r"C:\path\to\output_sheets"
FONT_PATH = r"C:\Windows\Fonts\arial.ttf"
REFERENCE_WIDTH = 2560
REFERENCE_HEIGHT = 1440
FONT_SIZE = 75
THUMBNAIL_PADDING = 10
THUMBNAILS = 8

--------------------------------------------------------------------------------------------------

 **Usage**

Place your video files in the Videos folder.

Run the script:

BVCS script.py

Contact sheets will be saved in the output_sheets folder.

 Output Example

A 2560x1440 image with 8 thumbnails.

Metadata displayed at the top.

Dynamic resizing for square or non-standard aspect ratios.

--------------------------------------------------------------------------------------------------

 **Troubleshooting**

FileNotFoundError during cleanup: Fixed by ensuring only existing thumbnails are removed.

Timeouts: Thumbnail generation has a 10-second timeout per frame.

Missing Thumbnails: If fewer than 8 thumbnails are generated, the last valid thumbnail is repeated.

--------------------------------------------------------------------------------------------------

 **License**

MIT License. See LICENSE for more information.

--------------------------------------------------------------------------------------------------

 **Contact**

For questions or support, reach out via GitHub Issues.
