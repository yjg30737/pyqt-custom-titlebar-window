import os.path, posixpath

from PyQt5.QtGui import QColor, QPalette, qGray, QIcon
from PyQt5.QtWidgets import QGraphicsColorizeEffect, QWidget, QApplication, QPushButton

from pyqt_custom_titlebar_window import SRC_DIR
from pyqt_custom_titlebar_window.button_style_helper import ButtonStyleHelper


class Button(QPushButton):
    def __init__(self, base_widget: QWidget = None, parent=None):
        super().__init__(parent)
        self.style_helper = ButtonStyleHelper(base_widget)
        self.setStyleSheet(self.style_helper.styleInit())
        self.installEventFilter(self)

    def setStyleAndIcon(self, icon: str):
        self.style_helper.__icon = path.join(SRC_DIR, icon)
        self.setStyleSheet(self.style_helper.styleInit())
        self.setIcon(QIcon(icon))

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == 98:  # Event type for EnableChange
                effect = QGraphicsColorizeEffect()
                effect.setColor(QColor(255, 255, 255))
                if self.isEnabled():
                    effect.setStrength(0)
                else:
                    effect.setStrength(1)
                    effect.setColor(QColor(150, 150, 150))
                self.setGraphicsEffect(effect)
        return super().eventFilter(obj, event)

    def setBackground(self, background=None):
        self.style_helper.setBackground(background)