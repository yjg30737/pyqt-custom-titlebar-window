# pyqt-custom-titlebar-window

PyQt custom titlebar window(resizable, movable, minimize/maximize/close). 

User can set modernized and customized frame surrounding the widget you made.

You can set the title bar separately or set the menu bar as title bar.

Basic buttons like min/max/close are automatically set by user's OS.

You can set your customized buttons(e.g. min/max/close).

You can drag title bar or menu bar on widget to move the window, double-click it to show maximize/normal.

This also makes the application's font look much better by setting the font family to 'Arial'(which looks modern and commonly used), antialiasing the font.

The range of font size is set to 9~12 which is not too big, not too small.

If you want to set custom titlebar easily than use <a href="https://github.com/yjg30737/pyqt-custom-titlebar-setter.git">pyqt-custom-titlebar-setter</a>.

If you want to use this in various ways than use this directly. see the example below.

## Table of Contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Included Packages](#included-packages)
* [Feature](#feature)
* [Example](#example)
   * [Code Sample (Menu bar only)](#code-sample-menu-bar-only)
   * [Code Sample (Including title bar)](#code-sample-including-title-bar)

## Requirements
PyQt5 >= 5.15 - This package is using <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemMove">startSystemMove</a>, <a href="https://doc.qt.io/qt-5/qwindow.html#startSystemResize">startSystemResize</a> which were both introduced in Qt 5.15.

## Setup
`python -m pip install pyqt-custom-titlebar-window`

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-frameless-window.git">pyqt-frameless-window</a> - To import parent class `FramelessWindow`
* <a href="https://github.com/yjg30737/pyqt-windows-buttons-widget.git">pyqt-windows-buttons-widget</a> - To provide Windows 10 OS style min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-mac-buttons-widget.git">pyqt-mac-buttons-widget</a> - To provide macOS style of min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-top-titlebar-widget.git">pyqt-top-titlebar-widget</a> - For adding top title bar feature
* <a href="https://github.com/yjg30737/pyqt-svg-label.git">pyqt-svg-label</a> - For setting icon/title to menu bar if user shows menu bar only

## Feature
* If you drag the frame, window will be resized.
* If you drag the title bar(menu bar if there is no title bar) of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* Set the window title by itself if you set your inner widget's title with `setWindowTitle`. It also catches the `windowTitleChanged` signal of your inner widget.
* Support close event(QCloseEvent) of inner widget.
* Support full screen feature. When full screen feature turns on, top title bar will disappear. Reappear when it turns off.
* `CustomTitlebarWindow(CustomizedWidgetByUser())` - Constructor.
* `setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 14), align=Qt.AlignCenter, bottom_separator=False)` to set title bar on the top of the window.
* `setButtons(btnWidget=None, align=Qt.AlignRight)` to add buttons(e.g. min/max/close) on the top right/left corner of title/menu bar. If `btnWidget` is set to None, buttons' style are automatically set to your platform/OS friendly style. Basically you can give `btnWidget` to your customized buttons(<a href= "https://github.com/yjg30737/pyqt-titlebar-buttons-widget.git">pyqt-titlebar-buttons-widget</a>). I will explain it better. Sorry for weak explanation.
* `setButtonHint(hint)` to set hints of buttons. There are three options available(close, min/close, min/max/close). Default value is min/max/close.
* `setMenuAsTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 9))` to set the icon and title not only on the left side of menu bar, but also set it as window icon and title.

Note: using this function, `macOS` button will be positioned to right which is unorthodox.
* Frame's color synchronizes with the `QMenuBar`'s background color or inner `QWidget`'s color if inner widget is not `QMainWindow`.
* `getCornerWidget()` to get corner widget of `QMenuBar` easily
* `getInnerWidget()` to get inner widget easily

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
  customTitlebarWindow.setMenuAsTitleBar(icon_filename='calculator.svg')
  # customTitlebarWindow.setButtonHint(hint=['close'])
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()
```

In the code sample, <a href="https://github.com/yjg30737/pyqt-dark-calculator.git">pyqt-dark-calculator</a> is being used as inner widget.  

### Result
 
![image](https://user-images.githubusercontent.com/55078043/173995588-bd7c71c7-6d06-487d-8fc7-6ed6cb16c459.png)

Here's another example with <a href="https://github.com/yjg30737/pyqt-dark-notepad.git">pyqt-dark-notepad</a>.

![image](https://user-images.githubusercontent.com/55078043/173995673-e3a15af0-a0df-4a95-85e8-a52a6bc4af03.png)

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
  # customTitlebarWindow.setButtonHint(['close'])
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()
```

### Result

![image](https://user-images.githubusercontent.com/55078043/172531428-18f64493-d2a2-4a7c-ab46-8b84ff9b982c.png)
