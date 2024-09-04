from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, qApp
from pyqt_custom_titlebar_window.svgLabel import SvgLabel


class SvgIconTextWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__svgIconLbl = SvgLabel()

        self.__textLbl = QLabel()
        self.__textLbl.installEventFilter(self)

        self.__setIconSizeForFontSize()

        lay = QHBoxLayout()
        lay.addWidget(self.__svgIconLbl)
        lay.addWidget(self.__textLbl)

        self.setLayout(lay)

    def setSvgFile(self, filename: str):
        self.__svgIconLbl.setSvgFile(filename)

    def setText(self, text: str):
        self.__textLbl.setText(text)

    def getSvgLabel(self) -> SvgLabel:
        return self.__svgIconLbl

    def getTextLabel(self) -> QLabel:
        return self.__textLbl

    def __setIconSizeForFontSize(self):
        w = h = int(self.__textLbl.font().pointSize() * 1.5 * qApp.screens()[0].logicalDotsPerInch()//96.0)
        self.__svgIconLbl.setFixedSize(w, h)

    def eventFilter(self, obj, e):
        if obj == self.__textLbl:
            # font changed
            if e.type() == 97:
                self.__setIconSizeForFontSize()
        return super().eventFilter(obj, e)