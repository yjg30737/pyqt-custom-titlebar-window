# pyqt-custom-titlebar-window

PyQt custom titlebar window(resizable, movable, minimize/maximize/close). User can put customized widget in the frame. Drag title bar or menu bar on widget to move the window, double-click it to show maximize/normal.

If you want to set this easily than use <a href="https://github.com/yjg30737/pyqt-custom-titlebar-setter.git">pyqt-custom-titlebar-setter</a>. 

If you want to use this in various ways than see the example below.

## Table of Contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Included Packages](#included-packages)
* [Feature](#feature)
* [Example](#example)
   * [Code Sample (Menu bar only)](#code-sample-menu-bar-only)
   * [Code Sample (Including title bar)](#code-sample-including-title-bar)

## Requirements
PyQt5 >= 5.15

## Setup
`python -m pip install pyqt-custom-titlebar-window`

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-frameless-window.git">pyqt-frameless-window</a> - To import parent class `FramelessWindow`
* <a href="https://github.com/yjg30737/pyqt-windows-buttons-widget.git">pyqt-windows-buttons-widget</a> - To provide Windows 10 OS style min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-mac-buttons-widget.git">pyqt-mac-buttons-widget</a> - To provide macOS style of min/max/close buttons with menu bar
* <a href="https://github.com/yjg30737/pyqt-top-titlebar-widget.git">pyqt-top-titlebar-widget</a> - For adding top title bar feature
* <a href="https://github.com/yjg30737/python-get-absolute-resource-path.git">python-get-absolute-resource-path</a> - For get absoulte resource path of svg icon to set window icon

## Feature
* If you drag the frame, window will be resized.
* If you drag the title bar(menu bar if there is no title bar) of inner widget, window will be moved.
* If you double-click the menu bar, window will be maximized/normalized.
* Set the window title by itself if you set your inner widget's title with `setWindowTitle`. It also catches the `windowTitleChanged` signal of your inner widget.
* Support full screen feature. When full screen feature turns on, top title bar will disappear. Reappear when it turns off.
* `CustomTitlebarWindow(CustomizedWidgetByUser())` - Constructor.
* `setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 12), align=Qt.AlignCenter, bottom_separator=False)` to set title bar on the top of the window.
* `setButtons()` to add min/max/close button on the top right corner of title/menu bar
* `setButtonHint(hint)` to set hints of buttons. There are three options available(close, min/close, min/max/close). Default value is min/max/close.
* `setButtonStyle(style)` to set style of buttons, This accepts only two string('Windows', 'Mac').
* `setMenuTitle(title: str, icon_filename: str, font=QFont('Arial', 12))` to set the icon and title not only on the left side of menu bar, but also set it as window icon and title.
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
  # customTitlebarWindow.setButtonHint(hint=['close'])
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
  # customTitlebarWindow.setButtonHint(['close'])
  # customTitlebarWindow.setButtonStyle(style='Mac')
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()
```

### Result

![image](https://user-images.githubusercontent.com/55078043/154799161-912fa324-dbfd-469a-a1b6-e67d907eb828.png)
