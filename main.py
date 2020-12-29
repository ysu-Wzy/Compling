import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QMessageBox
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
        self.clear_variable_btn.clicked.connect(self.clear_variable)
        self.execute_btn.clicked.connect(self.execute)
        self.cal = Calculator()

    def cifa(self):
        try:
            string = self.input_textEdit.toPlainText()
            strings = string.split('\n')
            select_text = self.input_textEdit.textCursor().selectedText()
            if select_text == "":  # 如果没有选中的文本,就选取最后一行执行
                select_text = strings[-1]
            # if len(select_text.split('\n')) > 1:
            #     QMessageBox.information(self, "", "最多选择一行", QMessageBox.Yes | QMessageBox.No)
            tokens = self.cal.cifa(select_text)
            self.show_textBrowser.append(select_text + "  词法分析结果：\n" + str(tokens))
            self.show_textBrowser.append("\n".join(self.cal.cifa_dec))
            self.show_textBrowser.append("---------------------")
            self.yufa_btn.setEnabled(True)
        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))
            self.show_textBrowser.append("---------------------")

    def yufa(self):
        try:
            wenfa = self.cal.yufa()
            self.show_textBrowser.append("语法分析结果：\n" + "\n".join(wenfa))
            self.after_btn.setEnabled(True)
            self.front_btn.setEnabled(True)
            self.show_textBrowser.append("---------------------")
        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))
            self.show_textBrowser.append("---------------------")

    def calculate_after(self):
        try:
            expression, result = self.cal.calculate(type='after')
            self.show_textBrowser.append("后缀表达式为:" + str(expression))
            self.show_textBrowser.append("结果为:" + str(result))
            self.show_textBrowser.append("---------------------")
            self.show_word_dict()
        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))
            self.show_textBrowser.append("---------------------")

    def calculate_front(self):
        try:
            expression, result = self.cal.calculate(type='front')
            self.show_textBrowser.append("前缀表达式为:" + str(expression))
            self.show_textBrowser.append("结果为:" + str(result))
            self.show_textBrowser.append("---------------------")
            self.show_word_dict()
        except Exception as e:
            self.show_textBrowser.append("<font color = red>%s</font>" % str(e))
            self.show_textBrowser.append("---------------------")

    def clear_result(self):
        self.show_textBrowser.clear()

    def input_changed(self):
        self.yufa_btn.setEnabled(False)
        self.after_btn.setEnabled(False)
        self.front_btn.setEnabled(False)

    def show_word_dict(self):
        for id, item in enumerate(self.cal.word_dict):
            # self.cal.show_value_table[item] = self.cal.calculate(type='after', tokens=self.cal.token_value_table[item])[1]
            if id == 0:
                self.value_show_textBrowser.setText(item + ":" + str(self.cal.word_dict[item]))
            else:
                self.value_show_textBrowser.append(item + ":" + str(self.cal.word_dict[item]))

    def clear_variable(self):
        self.value_show_textBrowser.clear()
        self.cal.word_dict = {}
        self.show_textBrowser.append('清空变量成功!')
        self.show_textBrowser.append("---------------------")

    def execute(self):
        string = self.input_textEdit.toPlainText().strip()

        select_text = self.input_textEdit.textCursor().selectedText()
        if select_text == "":  # 若选中为空，则执行所有
            strings = string.split('\n')
        else:  # 否则执行选中的区域
            strings = select_text.split('\n')

        for id, line in enumerate(strings):
            try:
                tokens = self.cal.cifa(line)  # 词法分析
                wenfa = self.cal.yufa()  # 语法分析
                expression, result = self.cal.calculate(type='after', tokens=tokens)
                if id == len(strings) - 1:
                    self.show_textBrowser.append("运行成功!")
                    self.show_textBrowser.append("---------------------")
            except Exception as e:
                self.show_textBrowser.append("<font color = red>第%s行%s</font>" % (id + 1, str(e)))
                self.show_textBrowser.append("---------------------")
                break
        self.show_word_dict()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QWidget()
    ui = My_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
