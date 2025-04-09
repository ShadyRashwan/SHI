# SHI - Images to PDF Converter

## 📋 Overview

   SHI is a powerful utility that converts images in folders and subfolders to PDF documents. It's designed to help you organize and archive your image collections efficiently by creating a consolidated PDF file for each folder of images.


```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                          ███████╗██╗  ██╗██╗                     ║
║                          ██╔════╝██║  ██║██║                     ║
║                          ███████╗███████║██║                     ║
║                          ╚════██║██╔══██║██║                     ║
║                          ███████║██║  ██║██║                     ║
║                          ╚══════╝╚═╝  ╚═╝╚═╝                     ║
║                                                                  ║
║                                                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## ✨ Features

- **Comprehensive Format Support**: Handles all common image formats (JPG, PNG, GIF, BMP, TIFF) and even Apple HEIC files
- **Recursive Processing**: Automatically processes images in subfolders
- **Aspect Ratio Preservation**: Maintains image proportions in the generated PDF
- **Progress Tracking**: Visual progress bars during processing
- **Option to Preserve Originals**: Choose whether to keep or delete original images
- **Clean User Interface**: Simple interactive command-line interface

## 📊 How It Works

Input a folder path, the tool will process it and process sub-folders if any.

![SHI Logo](shi.png)


## 🚀 Installation (Detailed Guide)

SHI requires **Python 3.6+**. You can install dependencies using **Conda**, **pip**, or a **Python virtual environment (`venv`)**. Choose the method that works best for you.

---

### 🐧 Mac / Linux

#### 1. Open Terminal
- Go to `Applications > Utilities > Terminal` or press `Cmd + Space` and search for **Terminal**.

#### 2. Clone the repository
```bash
git clone https://github.com/username/SHI.git
cd SHI
```

#### 3. Choose one of the following setup options:

##### 👉 Option A: Using Conda (Recommended)
```bash
conda env create -f env.yml
conda activate shi
```

##### 👉 Option B: Using Python Virtual Environment (`venv`)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

##### 👉 Option C: Using pip (No virtual environment)
```bash
pip install -r requirements.txt
```

---

### 🪟 Windows

#### 1. Open Command Prompt
- Press `Win + R`, type `cmd`, and press **Enter**.

#### 2. Install Git (if not already installed)
- Download from [https://git-scm.com](https://git-scm.com) and install (default options are fine).
- After installation, reopen Command Prompt.

#### 3. Clone the repository
```cmd
git clone https://github.com/username/SHI.git
cd SHI
```

#### 4. Choose one of the following setup options:

##### 👉 Option A: Using Conda (Recommended)
```cmd
conda env create -f env.yml
conda activate shi
```

##### 👉 Option B: Using Python Virtual Environment (`venv`)
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

##### 👉 Option C: Using pip (No virtual environment)
```cmd
pip install -r requirements.txt
```

---

## 💻 Usage

### Mac/Linux

1. Open Terminal.
2. Navigate to the SHI directory:
   ```bash
   python medical.py
   ```

### Windows

1. Run the Python script:
   ```cmd
   python medical.py
   ```

## 📝 Usage Instructions

1. When prompted, enter the full path to the folder containing your images.
2. Choose whether to preserve original images or delete them after PDF creation.
3. The tool will process all images in the folder and its subfolders.
4. PDFs will be created in each folder, named after the folder.

## 📊 Supported Image Formats

| Format | Extension | Support |
|--------|-----------|---------|
| JPEG   | .jpg, .jpeg | ✅ |
| PNG    | .png      | ✅ |
| GIF    | .gif      | ✅ |
| BMP    | .bmp      | ✅ |
| TIFF   | .tiff, .tif | ✅ |
| HEIC   | .heic     | ✅ (auto-converts to PNG) |

## ⚠️ Important Notes

- By default, original images will be deleted after processing
- Make a backup of your images if needed before running the tool
- The tool creates one PDF per folder, named after the folder

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Made with ❤️ by Shady Rashwan
- Created: March 12, 2023

---

