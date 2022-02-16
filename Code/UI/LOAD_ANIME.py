from PyQt5.QtCore import pyqtProperty, QSize, Qt, QRectF, QTimer, QRect
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import *

class PercentProgressBar(QWidget):
    MinValue = 0
    MaxValue = 100
    Value = 0
    BorderWidth = 8
    Clockwise = True
    ShowPercent = True
    ShowFreeArea = False
    ShowSmallCircle = False
    TextColor = QColor(255, 255, 255)
    BorderColor = QColor(24, 189, 155)
    BackgroundColor = QColor(70, 70, 70)

    def __init__(self, *args, value=0, minValue=0, maxValue=100,
                 borderWidth=8, clockwise=True, showPercent=True,
                 showFreeArea=False, showSmallCircle=False,
                 textColor=QColor(255, 255, 255),
                 borderColor=QColor(24, 189, 155),
                 backgroundColor=QColor(70, 70, 70), **kwargs):
        super(PercentProgressBar, self).__init__(*args, **kwargs)
        self.Value = value
        self.MinValue = minValue
        self.MaxValue = maxValue
        self.BorderWidth = borderWidth
        self.Clockwise = clockwise
        self.ShowPercent = showPercent
        self.ShowFreeArea = showFreeArea
        self.ShowSmallCircle = showSmallCircle
        self.TextColor = textColor
        self.BorderColor = borderColor
        self.BackgroundColor = backgroundColor

    def setRange(self, minValue: int, maxValue: int):
        if minValue >= maxValue:
            return
        self.MinValue = minValue
        self.MaxValue = maxValue
        self.update()

    def paintEvent(self, event):
        super(PercentProgressBar, self).paintEvent(event)
        width = self.width()
        height = self.height()
        side = min(width, height)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing)
        painter.translate(width / 2, height / 2)
        painter.scale(side / 100.0, side / 100.0)

        self._drawCircle(painter, 50)
        self._drawArc(painter, 50 - self.BorderWidth / 2)
        self._drawText(painter, 50)

    def _drawCircle(self, painter: QPainter, radius: int):
        radius = radius - self.BorderWidth
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.BackgroundColor)
        painter.drawEllipse(QRectF(-radius, -radius, radius * 2, radius * 2))
        painter.restore()

    def _drawArc(self, painter: QPainter, radius: int):
        painter.save()
        painter.setBrush(Qt.NoBrush)
        pen = painter.pen()
        pen.setWidthF(self.BorderWidth)
        pen.setCapStyle(Qt.RoundCap)

        arcLength = 360.0 / (self.MaxValue - self.MinValue) * self.Value
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)

        if not self.Clockwise:
            arcLength = -arcLength

        if self.ShowFreeArea:
            acolor = self.BorderColor.toRgb()
            acolor.setAlphaF(0.2)
            pen.setColor(acolor)
            painter.setPen(pen)
            painter.drawArc(rect, (0 - arcLength) *
                            16, -(360 - arcLength) * 16)

        pen.setColor(self.BorderColor)
        painter.setPen(pen)
        painter.drawArc(rect, 0, -arcLength * 16)

        if self.ShowSmallCircle:
            offset = radius - self.BorderWidth + 1
            radius = self.BorderWidth / 2 - 1
            painter.rotate(-90)
            circleRect = QRectF(-radius, radius + offset,
                                radius * 2, radius * 2)
            painter.rotate(arcLength)
            painter.drawEllipse(circleRect)

        painter.restore()

    def _drawText(self, painter: QPainter, radius: int):
        painter.save()
        painter.setPen(self.TextColor)
        painter.setFont(QFont('Arial', 25))
        strValue = '{}%'.format(int(self.Value / (self.MaxValue - self.MinValue)
                                    * 100)) if self.ShowPercent else str(self.Value)
        painter.drawText(QRectF(-radius, -radius, radius * 2,
                                radius * 2), Qt.AlignCenter, strValue)
        painter.restore()

    @pyqtProperty(int)
    def minValue(self) -> int:
        return self.MinValue

    @minValue.setter
    def minValue(self, minValue: int):
        if self.MinValue != minValue:
            self.MinValue = minValue
            self.update()

    @pyqtProperty(int)
    def maxValue(self) -> int:
        return self.MaxValue

    @maxValue.setter
    def maxValue(self, maxValue: int):
        if self.MaxValue != maxValue:
            self.MaxValue = maxValue
            self.update()

    @pyqtProperty(int)
    def value(self) -> int:
        return self.Value

    @value.setter
    def value(self, value: int):
        if self.Value != value:
            self.Value = value
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        self._value = 0
        self._widgets = []
        self._timer = QTimer(self, timeout=self.updateValue)
        self._widgets.append(PercentProgressBar(self))
        layout.addWidget(self._widgets[0])
        self._timer.start(20)
        self.count = 0

        self.mes_show_Q = QTextEdit(self)
        self.mes_show_Q.setGeometry(QRect(300, 350, 300, 40))
        self.mes_show_Q.setObjectName("mes_show_Q")
        self.mes_show_Q.show()

    def updateValue(self):
        for w in self._widgets:
            w.value = self._value
        self._value += 1
        if self.count == 0:
            self.mes_show_Q.setText("Sending...")
            self.mes_show_Q.show()
        if self.count == 1:
            self.mes_show_Q.setText("Delivering...")
            self.mes_show_Q.show()
        if self.count == 2:
            self._widgets[0].hide()
            self.mes_show_Q.setGeometry(QRect(110, 200, 200, 40))
            self.mes_show_Q.setText("Send Accomplished！")
        if self.count == 3:
            self.close()
        if self._value > 100:
            self._value = 0
            self.count += 1


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Window()
    w.resize(400,400)
    w.show()
    sys.exit(app.exec_())