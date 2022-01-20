# pyqt-custom-frame
PyQt Custom Frame(resizable). User can put customized widget(QMainWindow only) in the frame. Drag menu bar on QMainWindow to move the window, double-click it to maximize/normalize. 

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-frame.git --upgrade```

## Usage
Give your customized widget to the constructor like this. ```CustomFrame(CustomizedWidgetByUser())```

## Feature
* If you drag the frame, window will be resized.
* If you drag the menu bar of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.

## Note
On version v0.1.0, type of inner widget should be QMainWindow.

## Example
### Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_custom_frame import CustomFrame
from pyqt_dark_notepad import DarkNotepad


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    systemSpecificCustomFramelessMainWindow = CustomFrame(DarkNotepad()) # DarkNotepad is main class of pyqt-dark-notepad
    systemSpecificCustomFramelessMainWindow.show()
    app.exec_()
```

<a href="https://github.com/yjg30737/pyqt-dark-notepad.git">pyqt-dark-notepad</a>

### Result

![image](https://user-images.githubusercontent.com/55078043/150244463-7558e45d-4450-4422-91a2-4c85d806c996.png)

