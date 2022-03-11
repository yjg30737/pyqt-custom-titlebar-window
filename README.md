# pyqt-custom-titlebar-window

PyQt Custom Titlebar Window (resizable, movable, minimize/maximize/close). User can put customized widget in the frame. Drag title bar or menu bar on widget to move the window, double-click it to show maximize/normal.

## Table of Contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Included Packages](#included-packages)
* [Feature](#feature)
* [Example](#example)
   * [Code Sample (Menu bar only)](#code-sample-menu-bar-only)
   * [Code Sample (Including title bar)](#code-sample-including-title-bar)
* [Release Note](#release-note)

## Requirements
PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-custom-titlebar-window.git --upgrade```

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-frameless-window.git">pyqt-frameless-window</a> - To import parent class ```FramelessWindow``` 
* <a href="https://github.com/yjg30737/pyqt-windows-min-max-close-buttons-widget.git">pyqt-windows-min-max-close-buttons-widget</a> - To provide Windows 10 OS style min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-mac-min-max-close-buttons-widget.git">pyqt-mac-min-max-close-buttons-widget</a> - To provide macOS style of min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-top-titlebar-widget.git">pyqt-top-titlebar-widget</a> - For adding top title bar feature
* <a href="https://github.com/yjg30737/python-get-absolute-resource-path.git">python-get-absolute-resource-path</a> - For get absoulte resource path of svg icon to set window icon

## Feature
* If you drag the frame, window will be resized.
* If you drag the title bar(menu bar if there is no title bar) of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* Set the window title by itself if you set your inner widget's title with ```setWindowTitle```. It also catches the ```windowTitleChanged``` signal of your inner widget.
* Support full screen feature. When full screen feature turns on, top title bar will disappear. Reappear when it turns off.
* ```CustomTitlebarWindow(CustomizedWidgetByUser())``` - Constructor.
* ```setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 12), align=Qt.AlignCenter, bottom_separator=False)``` to set title bar on the top of the window.
* ```setButtons()``` to add min/max/close button on the top right corner of title/menu bar
* ```setButtonHint(hint)``` to set hints of buttons. There are three options available(close, min/close, min/max/close). Default value is min/max/close.
* ```setButtonStyle(style)``` to set style of buttons, This accepts only two string('Windows', 'Mac').
* Frame's color synchronizes with the ```QMenuBar```'s background color or inner ```QWidget```'s color if inner widget is not ```QMainWindow```.
* ```getCornerWidget()``` to get corner widget of ```QMenuBar``` easily
* ```getInnerWidget()``` to get inner widget easily

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
  # customTitlebarWindow.setButtonHint(hint=Qt.WindowCloseButtonHint)
  # customTitlebarWindow.setButtonStyle(style='Mac')
  customTitlebarWindow.setButtons()
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
  # customTitlebarWindow.setButtonHint(hint=Qt.WindowCloseButtonHint)
  # customTitlebarWindow.setButtonStyle(style='Mac')
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()
```

### Result

![image](https://user-images.githubusercontent.com/55078043/154799161-912fa324-dbfd-469a-a1b6-e67d907eb828.png)

## Release Note
(Start from 0.5.0)
### February 27, 2021 (version 1.3.1)

Fix the bug(which occurs when user double-clicks the title bar) caused by collision between two events(```mousePressEvent```, ```mouseDoubleClickEvent```) by setting the ```bool``` type ```pressToMove``` variable ```False```, Add method for specific case(```setPressToMove```).

### February 22, 2021 (version 1.3.0)

Rename one of the method ```setMinMaxCloseButton``` to ```setButtons```.

Let user set the hint and style of buttons with ```setButtonHint(hint)```, ```setButtonStyle(style)```.

### February 21, 2021 (version 1.2.1)

Make this able to handle not only ```QMainWindow```, but also ```QWidget```, ```QDialog``` to enhance flexibility

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
