# Steganography

## 📝 Description

Steganography is a method of hiding one piece of information inside another, making the hidden content seem harmless. Unlike encryption that makes data unreadable, steganography focuses on secrecy by keeping the hidden information undetected.

I have developed a Python program that can hide a message or file within an image without being detected. The message can be in the form of text or any type of file.

## 🏗️ Implementation

Python was chosen as the programming language for this task because it provides easy handling of binary files.

The process of embedding a hidden message is as follows:

1. Encrypt the file or string to be embedded using the AES cipher with the CBC block mode.
2. Load the image that will contain the embedded message using the Pillow library.
3. Embed the binary data of the encrypted string or file into the least significant bits of the pixels in the image.
4. Each pixel in the image consists of 3 bytes (representing the RGB color channels), allowing for 3 bits of secret information to be hidden in each pixel.
5. The binary data includes a header that contains information such as the content type (string or file) and its size.

The resulting output image closely resembles the input image and is indistinguishable to the human eye.

## 🧑‍🔬 Technologies

- [Python 3](https://www.python.org/downloads/)
- [Pillow](https://pypi.org/project/Pillow/)
- [PyCryptodome](https://pypi.org/project/pycryptodome/)

## 🔨 Usage

### Installation

- Install Python 3 (if not installed).
- Activate virtual environment (optional).
    ```bash
    python -m venv venv # create virtual environment
    source venv/bin/activate # activate virtual environment
    ```
- Install necessary dependencies using this command.
    ```bash
    pip install -r requirements.txt
    ```

### Help

- Run help command
    ```
    python steganography.py -h

    usage: steganography.py [-h] [-e] [-x] [-p PASSWORD] [-i INPUT_FILE] [-f FILE_CONTENT] [-s STRING_CONTENT] [-o OUTPUT_FILE]

    Steganography

    options:
    -h, --help            show this help message and exit
    -e, --embed           Embed data to input image.
    -x, --extract         Extract data from input image.
    -p PASSWORD, --password PASSWORD
                            Secret password for encryption and decryption (max length is 16).
    -i INPUT_FILE, --input-file INPUT_FILE
                            File to embed data into or extract data from.
    -f FILE_CONTENT, --file-content FILE_CONTENT
                            File content to embed.
    -s STRING_CONTENT, --string-content STRING_CONTENT
                            String to embed into the input image.
    -o OUTPUT_FILE, --output-file OUTPUT_FILE
                            Output file that will contain the embedded file in case of embedding, extracted data in case of extracting
    ```

### Hide message

- How to hide (embed) a **string** to the image called wallpaper.jpg
    ```bash
    python steganography.py \
        --embed \
        --input-file wallpaper.jpg \
        --output-file wallpaperWithMessage \
        --string-content "This is the secret message" \
        --password '5340mllJKlkdfs90'
    ```

- How to hide a **file** called secret.jpg to the image called wallpaper.jpg
    ```bash
    python steganography.py \
        --embed \
        --input-file wallpaper.jpg \
        --output-file wallpaperWithMessage \
        --file-content secret.jpg \
        --password '5340mllJKlkdfs90'
    ```

### Retrieve message

- How to retrieve (extract) a hidden message from the image called wallpaper.png
    ```bash
    python steganography.py \
        --extract \
        --input-file wallpaperWithMessage.jpg \
        --password '5340mllJKlkdfs90'
    ```