## What is PyVutils ?

PyVutils (Vic Utilities for Python) is a comprehensive utility library written in Python that provides a rich set of tools and wrapper functions to simplify common programming tasks. This is not a wrapper of [Vutils](https://github.com/vic4key/Vutils.git) but a standalone Python library designed to make your development workflow easier, faster, and more efficient.

## Features

* **Cross-Platform Support**: Compatible with both `Python 2` & `Python 3`
* **Computer Vision**: OpenCV wrapper with simplified image/video processing, webcam capture, and 2D convolution filters
* **Web Automation**: Browser automation with mechanize, proxy server implementation, and HTTP utilities
* **File System Operations**: Comprehensive file/directory manipulation, path utilities, and I/O operations
* **Network Programming**: HTTP handling, web scraping capabilities, and proxy server functionality
* **Audio/Sound Control**: System speaker control and audio manipulation (Windows)
* **Mathematical Utilities**: Mathematical functions and Point2D class for geometric operations
* **Security & Cryptography**: Cryptographic utilities and security functions
* **Medical Imaging**: DICOM file processing and medical image handling
* **Process & Threading**: Process management and threading utilities
* **Caching System**: LRU cache implementation and caching mechanisms
* **Text Processing**: String manipulation and text utilities
* **Debug & Profiling**: Exception logging, performance profiling decorators, and debug utilities
* **Windows Integration**: Windows-specific functionality and system integration
* **Modular Design**: Well-organized modules for specific functionality domains

## Installation

`pip install git+https://github.com/vic4key/PyVutils.git`

## Usage

```python
# Examples

import PyVutils as vu

# system speakers

speaker = vu.Speaker()
speaker.set_volume_level(70)
speaker.mute()

# open cv

def callback(frame, info, *args):
    return frame

vu.webcam(callback)
vu.play_video("path\to\video\file", callback)

# web browser

browser = vu.WebBrowser()
browser.open("https://cold-dream-9470.bss.design")
print(browser.title())
for form in browser.forms():
    print(form)

# file / directory

def callback(file_path, file_directory, file_name):
    print("`%s` - `%s` - `%s`" % (file_path, file_directory, file_name))

vu.recursive_directory(".", callback, ["txt"])

# others

@vu.profiling
def func():
    time.sleep(1)

# etc
```

## Contact
Feel free to contact via [Twitter](https://twitter.com/vic4key) or [Gmail](mailto:vic4key@gmail.com) or [Blog](https://vic.onl/)
