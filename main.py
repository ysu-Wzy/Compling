import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from calculator_ui import Ui_Form
from calculator import Calculator


class My_ui(Ui_Form):

    def __init__(self, QWidget):
        super().setupUi(QWidget)
        self.cifa_btn.clicked.connect(self.cifa)
        self.yufa_btn.clicked.connect(self.yufa)
        self.clearReuslt_btn.clicked.connect(self.clear_result)
        self.after_btn.clicked.connect(self.calculate_after)
        self.input_textEdit.textChanged.connect(self.input_changed)
        self.front_btn.clicked.connect(self.calculate_front)
        self.cal = Calculator()


    def cifa(self):
        try:
            string = self.input_textEdit.toPlainText()
            tokens = self.cal.cifa(string)
            self.show_textBrowser.append("词法分析结果：\n" + str(tokens))
            self.show_textBrowser.append("\n".join(self.cal.cifa_dec))
            self.show_textBrowser.append("---------------------")
            self.yufa_btn.setEnabled(True)
        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>"%str(e))
            # self.show_textBrowser.append("词法分析出现错误")
            self.show_textBrowser.append("---------------------")

    def yufa(self):
        try:
            wenfa = self.cal.yufa()
            self.show_textBrowser.append("语法分析结果：\n" + "\n".join(wenfa))
            self.after_btn.setEnabled(True)
            self.front_btn.setEnabled(True)
            self.show_textBrowser.append("---------------------")

        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>"%str(e))
            self.show_textBrowser.append("---------------------")

    def calculate_after(self):
        try:
            expression, result = self.cal.calculate(type='after')
            self.show_textBrowser.append("后缀表达式为:" + str(expression))
            self.show_textBrowser.append("结果为:" + str(result))
            self.show_textBrowser.append("---------------------")
        except IndexError as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))

    def calculate_front(self):
        try:
            expression, result = self.cal.calculate(type='front')
            self.show_textBrowser.append("前缀表达式为:" + str(expression))
            self.show_textBrowser.append("结果为:" + str(result))
            self.show_textBrowser.append("---------------------")
        except IndexError as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))

    def clear_result(self):
        self.show_textBrowser.clear()

    def input_changed(self):
        self.yufa_btn.setEnabled(False)
        self.after_btn.setEnabled(False)
        self.front_btn.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QWidget()
    ui = My_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
