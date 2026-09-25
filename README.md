# **Local HEIC to JPG Converter**

A lightweight, privacy-focused desktop application that converts Apple HEIC images to high-quality JPGs. All conversions run locally on your machine with zero network calls. The setup requires no administrator rights and runs entirely in user space.
Features

    Local processing: Your images never leave your machine.

    Zero admin required: Installs and executes entirely in user space.

    Metadata preservation: Retains EXIF data, orientation, and capture timestamps.

    Color profile mapping: Converts HEIC profiles to standard RGB to avoid washed-out results.

    Batch conversion: Select individual files or convert an entire directory at once.

    Non-blocking GUI: Runs tasks on a background thread to keep the window responsive.

**Requirements**

    Python 3.8+

    Packages: pillow, pillow-heif

# **Installation**
Clone the repository:
Bash

git clone https://github.com/TheCanadianYeti/heicToJpg.git
cd heicToJpg

# **Option 1: Quick Install (Easiest)**

Install the required packages directly to your user folder with a single command:
Bash

python -m pip install --user pillow pillow-heif

# **Option 2: Virtual Environment**

If you prefer to keep dependencies isolated to this project folder:

Windows (PowerShell):
PowerShell

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pillow pillow-heif

Linux / macOS:
Bash

python3 -m venv .venv
source .venv/bin/activate
pip install pillow pillow-heif

# **Standalone Windows Executable (Easiest)          (.exe to be uploaded soon)** 

If you want to use the app without installing Python or running any terminal commands:

    Go to the Releases page.

    Download HeicToJpgConverter.exe from the latest release.

    Double-click the downloaded file to run it immediately.

# **Usage**

    Launch the application:
    Bash

    python _main_.py

    Select your input:

        Click "Select HEIC Files" to choose individual images.

        Click "Or Select Folder with HEIC" to batch process a directory.

    Select your output folder (optional):

        Click "Select Output Folder" to set a custom destination.

        If left unselected, JPGs save in the same directory as their source HEIC files.

    Click "Convert to JPG".
    

