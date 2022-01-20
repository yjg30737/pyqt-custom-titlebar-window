# pyqt-custom-frame
PyQt Custom Frame(resizable). User can put customized widget(QMainWindow only) in the frame. Drag menu bar on QMainWindow to move the window, double-click it to maximize/normalize. 

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-frame.git --upgrade```

## Usage
Give your customized widget to the constructor like ```CustomFrame(CustomizedWidgetByUser())```.

## Feature
* If you drag the frame, window will be resized.
* If you drag the menu bar of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* <b>v0.2.0 or above</b> - You can add min/max/close button on the top right corner of menu bar with ```setMinMaxCloseButton```. 

## Note
Type of inner widget should be QMainWindow.

## Example
### Code Sample
```python
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqt_custom_frame import CustomFrame


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    customFrameExample = CustomFrame(QMainWindow())
    customFrameExample.setMinMaxCloseButton()
    customFrameExample.show()
    app.exec_()
```

### Result

![image](https://user-images.githubusercontent.com/55078043/150272696-023a9847-2304-4a3f-a2d2-00758bed7871.png)

