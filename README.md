## What is PyVutils ?

PyVutils or Vic Utilities for Python (not a wrapper of [Vutils](https://github.com/vic4key/Vutils.git)) is an utility library written in Python for Python. It helps your programming go easier, faster and simpler.

## Features

* Support both `Python 2` & `Python 3`

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
