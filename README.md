# pyqt-custom-frame
PyQt Custom Frame

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-frame.git --upgrade```

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

