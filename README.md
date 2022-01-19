# pyqt-custom-frame
PyQt Custom Frame

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-frame.git --upgrade```

## Example
Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_custom_frame import CustomFrame


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    systemSpecificCustomFramelessMainWindow = CustomFrame()
    systemSpecificCustomFramelessMainWindow.show()
    app.exec_()
```
