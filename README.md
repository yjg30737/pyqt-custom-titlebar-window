# pyqt-custom-titlebar-window
PyQt Custom Titlebar Window (resizable, movable, minimize/maximize/close). User can put customized widget(QMainWindow only) in the frame. Drag menu bar on QMainWindow to move the window, double-click it to show maximize/normal.

## Table of Contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Feature & Usage](#feature-usage)
* [Note](#note)
* [Example](#example)
   * [Code Sample (Menu bar only)](#code-sample-menu-bar-only)
   * [Code Sample (Including title bar)](#code-sample-including-title-bar)
* [Release Note](#release-note)

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-titlebar-window.git --upgrade```

## Included package
* <a href="https://github.com/yjg30737/pyqt-frameless-window.git">pyqt-frameless-window</a> - Parent widget
* <s><a href="https://github.com/yjg30737/python-color-getter.git">python-color-getter</a></s> - To get the complementary color of base ```QWidget``` to make the title ```QLabel``` conspicuous (since v1.0.0 this is not being used at all. Because ```pyqt-top-titlebar-widget``` package do the task instead.) 
* <a href="https://github.com/yjg30737/pyqt-windows-min-max-close-buttons-widget.git">pyqt-windows-min-max-close-buttons-widget</a> - To provide the min/max/close buttons with the Windows 10 OS style
* <a href="https://github.com/yjg30737/pyqt-mac-min-max-close-buttons-widget.git">pyqt-mac-min-max-close-buttons-widget</a> - To provide the min/max/close buttons with the macOS style
* <a href="https://github.com/yjg30737/pyqt-top-titlebar-widget.git">pyqt-top-titlebar-widget</a> - For adding top title bar feature (included since v1.0.0)

## Feature & Usage
* If you drag the frame, window will be resized.
* If you drag the menu bar of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* ```CustomTitlebarWindow(CustomizedWidgetByUser())``` - Constructor.
* Available to add min/max/close button on the top right corner of menu bar with ```setMinMaxCloseButton(hint=Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint, style='Windows')```. If you want to add close button only, give the value like ```setMinMaxCloseButton(hint=Qt.WindowCloseButtonHint)```. There are three options available(close, min/close, min/max/close). Default value is min/max/close. About ```style``` argument, This accepts only two string('Windows', 'Mac'). Buttons' style will be changed by given OS' style.  
* Set the window title by itself if you set your ```QMainWindow```'s title with ```setWindowTitle```. It also catches the ```windowTitleChanged``` signal of your ```QMainWindow```.
* Frame's color synchronizes with the ```QMenuBar```'s background color.
* Applied stylesheets of min/max/close are based on the common min/max/close button style of Windows 10. (I'm currently using Windows 10.) For example, when you place the mouse on top of the close button, close button's color will turn into red. No animation involved currently.
* ```setTopTitleBar``` to set title bar above the menu bar. You can set the font of title bar and icon(which not only becomes an icon next to the title bar, but becomes window icon at the same time.) and alignment of title layout. Note: In current version(v1.0.2), title bar style will set to Windows OS only.
    * <b>Below v1.0.0</b> - ```setTopTitleBar(icon: QIcon = QIcon(), font: QFont = QFont('Arial', 16), align=Qt.AlignCenter)```
    * <b>Since v1.0.0</b> - ```setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 12), align=Qt.AlignCenter)``` - I change the ```QIcon``` type argument to ```str``` type argument which is named ```icon_filename``` because as far as i know QIcon doesn't support svg file well. ```icon_filename``` will pass to ```TopTitleBarWidget``` class which is included in ```pyqt-top-titlebar-widget```. The class is main widget of the separate title bar and shows svg icon label nicely.
* ```getCornerWidget()``` to get corner widget of ```QMenuBar``` easily
* ```setMenuStyle(style: str = 'Windows')``` to set menu style based on style which should be name of the OS. You can either give the 'Windows' or 'Mac' to the argument. Windows is set by default.
### v1.1.0
```python
customTitlebarWindow = CustomTitlebarWindow(window)
customTitlebarWindow.setTopTitleBar()
customTitlebarWindow.setMinMaxCloseButton()
```
After v1.1.0, the correct order of calling method is ```setTopTitleBar -> setMinMaxCloseButton``` if you want to set top title bar and each min/max/close button on it.   

## Note
Type of inner widget should be ```QMainWindow```. Because without ```QMenuBar``` this won't work.

## Example
### Code Sample (Menu bar only)

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

![image](https://user-images.githubusercontent.com/55078043/151106910-0bce8fa2-0cad-425c-8dda-18196536c3ac.png)

Here's another example with <a href="https://github.com/yjg30737/pyqt-dark-notepad.git">pyqt-dark-notepad</a>.

![image](https://user-images.githubusercontent.com/55078043/151106977-76a169cc-bcaf-4a46-8771-9216ee583b9f.png)

As you see, existing corner widget doesn't matter.

### Code Sample (Including title bar)

#### v1.0.3

```python
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqt_custom_titlebar_window import CustomTitlebarWindow
from pyqt_dark_notepad import DarkNotepad

if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)
  window = DarkNotepad()
  customTitlebarWindow = CustomTitlebarWindow(window)
  customTitlebarWindow.setMinMaxCloseButton()
  customTitlebarWindow.setTopTitleBar(icon_filename='dark-notepad.svg')
  customTitlebarWindow.show()
  app.exec_()
```

#### v1.1.0

```python
from PyQt5.QtWidgets import QApplication
from pyqt_custom_titlebar_window import CustomTitlebarWindow
from pyqt_dark_notepad import DarkNotepad


if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)
  window = DarkNotepad()
  customTitlebarWindow = CustomTitlebarWindow(window)
  customTitlebarWindow.setTopTitleBar(icon_filename='dark-notepad.svg')
  customTitlebarWindow.setMinMaxCloseButton()
  customTitlebarWindow.show()
  app.exec_()
```

### Result

![image](https://user-images.githubusercontent.com/55078043/154799161-912fa324-dbfd-469a-a1b6-e67d907eb828.png)

## Release Note
(Start from 0.5.0)

### February 21, 2021 (version 1.1.0)

Set order of calling method(setTopTitleBar -> setMinMaxCloseButton) and make it able to set Mac style to top title bar

### February 19, 2021 (version 1.0.3)

Use the package(<a href="https://github.com/yjg30737/pyqt-top-titlebar-widget.git">pyqt-top-titlebar-widget</a>) to reduce redunancy and length of code.

### February 17, 2021 (version 0.9.0)

Use the package(<a href="https://github.com/yjg30737/pyqt-windows-min-max-close-buttons-widget.git">pyqt-windows-min-max-close-buttons-widget</a>) to making the windows 10 OS button code and reduce redundancy and length of code.

### February 15, 2021 (version 0.8.0)

Now this module uses the <a href="https://github.com/yjg30737/pyqt-mac-min-max-close-buttons-widget.git">pyqt-mac-min-max-close-buttons-widget</a> to make user able to set macOS style to each button(min/max/close).

### January 28, 2021 (version 0.6.0)

Now this module inherits the <a href="https://github.com/yjg30737/pyqt-frameless-window.git">pyqt-frameless-window</a> to reduce the redundancy.

<small>Note for release note: I update this release info if update information is really crucial to know.</small>
