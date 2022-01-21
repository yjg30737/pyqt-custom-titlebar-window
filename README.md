# pyqt-custom-titlebar-window
PyQt Custom Titlebar Window (resizable, movable, minimize/maximize/close). User can put customized widget(QMainWindow only) in the frame. Drag menu bar on QMainWindow to move the window, double-click it to show maximize/normal. 

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-titlebar-window.git --upgrade```

## Usage
Give your customized widget to the constructor like ```CustomTitlebarWindow(CustomizedWidgetByUser())```.

## Feature
* If you drag the frame, window will be resized.
* If you drag the menu bar of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* Available to add min/max/close button on the top right corner of menu bar with ```setMinMaxCloseButton```. 

## Note
Type of inner widget should be QMainWindow.

## Example
### Code Sample

```python
from PyQt5.QtWidgets import QApplication
from pyqt_custom_titlebar_window import CustomTitlebarWindow
from pyqt_dark_calculator import Calculator


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    customTitlebarWindow = CustomTitlebarWindow(Calculator())
    customTitlebarWindow.setMinMaxCloseButton()
    customTitlebarWindow.show()
    app.exec_()
```

In the code sample, <a href="https://github.com/yjg30737/pyqt-dark-calculator.git">pyqt-dark-calculator</a> is being used as inner widget.  

### Result

![image](https://user-images.githubusercontent.com/55078043/150296182-5d1b719b-c59c-44ec-963e-d32e497243a4.png)

