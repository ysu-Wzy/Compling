# -*- coding=utf-8 -*-
# PYTHON实现算术表达式的词法语法语义分析（编译原理应用）
# https://blog.csdn.net/QFire/article/details/81236928
from my_exception import *

letter = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
number = '0123456789'
operator_list = '+-*/()^%'  # 运算符

identifier = 1
digit = 2
operator = 3
# 运算符优先
ops_rule = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '//': 2,
    '^': 3
}
###################################        语法分析         #####################################
'''
基本文法：
M -> +E|-E|E
E -> TE~
E~ -> +TE~|-TE~|&
T -> FT~
T~ -> *FT~|/FT~|&|^FT~|%FT~|//FT~
F -> (E)|indentifer|digit
'''
'''
Indentifer： 标识符  digit：数字 M：表达式

项：T    因子：F
'''


class Calculator:
    def __init__(self):
        self.i = 0  # 栈指针
        self.dic = {}  # 符号表
        self.table = []  # 单词栈
        self.wenfa = []  # 字符串文法
        self.cifa_dec = []  # 词法分析的描述
        self.is_assign = False  # 是否为赋值语句
        self.key = None  # 如果是赋值语句，单词是什么

        self.word_dict = {}  # 单词表

    def reset(self):
        self.dic = {}
        self.table = []
        self.wenfa = []  # 字符串文法
        self.cifa_dec = []  # 词法分析的描述
        self.is_assign = False  # 是否为赋值语句
        self.key = None  # 如果是赋值语句，单词是什么

    #####################################        词法分析        ######################################
    def cifa(self, string):  # 词法分析
        self.reset()
        string = string.replace(" ", "")
        # 如果是赋值语句
        if '=' in string:
            try:
                left_str, right_str = string.split("=")  # 只能包含一个等号
            except:
                raise EqualSignError
            # 开头必须为字母
            if left_str[0] not in letter: raise IdentifierDefineError
            # 左侧必须为标识符
            for i in range(len(left_str)):
                if left_str[i] not in letter + number:
                    raise IdentifierDefineError(i, "标识符中必须由数字和字母组成")
            string = right_str
            self.key = left_str
            self.is_assign = True

        self.table = []
        print('')
        m = 0  # 数字或标识符的开始位置
        point = False  # 是否允许出现小数点
        state = None  # 1：为标识符 2：为数字串 3：为运算符
        next = False  # 当检测到“//”时要前进两次
        for i in range(len(string)):
            # if string[i]!="-":
            if next:
                next = False
                continue
            if string[i] in operator_list:  # 如果是运算符
                if state == identifier:  # state=1表明其前面的为标识符
                    self.cifa_dec.append(string[m:i] + '是标识符,类型码：1')
                    self.dic[string[m:i]] = identifier
                    self.table.append(string[m:i])
                elif state == digit:  # state=2表明其前面的为数字
                    self.cifa_dec.append(string[m:i] + '是数字，类型码：2')
                    self.dic[string[m:i]] = digit
                    self.table.append(string[m:i])
                    point = False
                if string[i] == '-':  # 负数
                    if i > 0:
                        if string[i - 1] == "(":
                            point = True
                            state = digit
                            continue
                    elif state == None:
                        point = True
                        state = digit
                        continue
                if string[i] == '+':  # 正数
                    if i > 0:
                        if string[i - 1] == "(":
                            point = True
                            state = digit
                            continue
                    elif state == None:
                        point = True
                        state = digit
                        continue
                if string[i:i + 2] == '//':
                    state = operator
                    self.cifa_dec.append(string[i:i + 2] + '是运算符，类型码：3')
                    self.dic[string[i:i + 2]] = operator
                    self.table.append(string[i:i + 2])
                    m = i + 2
                    next = True
                    continue
                m = i + 1
                state = operator
                self.cifa_dec.append(string[i] + '是运算符，类型码：3')
                self.dic[string[i]] = operator
                self.table.append(string[i])
            elif string[i] in number:  # 如果是数字
                if i == m:  # 是数字的第一个字符
                    point = True
                    state = digit
            elif string[i] in letter:  # 如果是字母
                if state == digit:  # 判断此时的状态，若state=2表明状态为无符号整数，而整数内不能包含字母，故报错
                    print('词法分析检测到错误,数字串中不能包含字母')
                    raise NumberError(i, string[i])
                if i == m:  # 判断此时的字母是否为标识符的第一个字母，若是则改变状态为标识符
                    state = identifier
                    point = False
            elif string[i] == '.':
                if point == True:
                    continue
                else:
                    print("小数点错误")
                    raise PointError(i)
            else:  # 当输入的字符均不符合以上判断，则说明为非法字符，故报错
                print('词法分析检测到非法字符')
                raise InvalidCharError(i, string[i])

        if state == identifier:  # 当字符串检查完后，若字符串最后部分为标识符，应将其print出来
            self.cifa_dec.append(string[m:] + '是标识符，类型码：3')
            self.dic[string[m:]] = identifier
            self.table.append(string[m:])
        elif state == digit:  # 若字符串最后部分为无符号整数，应将其print出来
            self.cifa_dec.append(string[m:] + '是数字，类型码：2')
            self.dic[string[m:]] = digit
            self.table.append(string[m:])
        self.table.append('#')
        print('字符栈:', self.table, '\n词法正确')
        return self.table

    def yufa(self):
        self.i = 0  # 指针归零
        self.wenfa = []
        self.m()
        return self.wenfa

    def m(self):  # PM程序
        if (self.table[self.i] == '+'):
            self.i += 1
            self.wenfa.append('M -> +E')
            self.e()
        elif (self.table[self.i] == '-'):
            self.i += 1
            self.wenfa.append('M -> -E')
            self.e()
        else:
            self.wenfa.append('M -> E')
            self.e()
        if (self.i is not len(self.table) - 1):  # 语法分析结束时，若单词栈指针与单词表长度不相等，报错
            print("\n语法分析程序检查到错误,'('前应该有运算符")
            raise EOFError(self.i)
        else:
            print('\n字符串语法是：')  # 若一切正确，则输出语法树文法
            for i in self.wenfa:
                print(i)
            print('语法正确')

    def e(self):  # PE程序
        self.wenfa.append('E -> TE\'')
        self.t()
        self.e1()

    def e1(self):  # PE1程序
        if (self.table[self.i] == '+'):
            self.i += 1
            self.wenfa.append('E\' -> +TE\'')
            self.t()
            self.e1()
        elif (self.table[self.i] == '-'):
            self.i += 1
            self.wenfa.append('E\' -> -TE\'')
            self.t()
            self.e1()
        else:
            self.wenfa.append('E\' -> &')

    def t(self):  # PT程序
        self.wenfa.append('T -> FT\'')
        self.f()
        self.t1()

    def t1(self):  # PT1程序
        if (self.table[self.i] == '*'):
            self.i += 1
            self.wenfa.append('T\' -> *FT\'')
            self.f()
            self.t1()
        elif (self.table[self.i] == '/'):
            self.i += 1
            self.wenfa.append('T\' -> /FT\'')
            self.f()
            self.t1()
        elif (self.table[self.i] == '^'):
            self.i += 1
            self.wenfa.append('T\' -> ^FT\'')
            self.f()
            self.t1()
        elif (self.table[self.i] == '%'):
            self.i += 1
            self.wenfa.append('T\' -> %FT\'')
            self.f()
            self.t1()
        elif (self.table[self.i] == '//'):
            self.i += 1
            self.wenfa.append('T\' -> //FT\'')
            self.f()
            self.t1()
        else:
            self.wenfa.append('T\' -> &')

    def f(self):  # PF程序
        if (self.table[self.i] == '('):
            self.wenfa.append('F -> (E)')
            self.i += 1
            self.e()
            if (self.table[self.i] != ')'):
                raise YufaError(position=self.i, dec='词法分析错误，该处应有“)”')
            self.i += 1
        elif (self.dic[self.table[self.i]] == identifier):
            self.wenfa.append('F -> identifier ' + str(self.table[self.i]))
            self.i += 1
        elif (self.dic[self.table[self.i]] == digit):
            self.wenfa.append('F -> Digit ' + str(self.table[self.i]))
            self.i += 1
        else:
            raise YufaError(self.i, "因子只能由(E)或者标识符或者数字组成，出错字符：{}，字符类型：{}".format(self.table[self.i], self.dic[
                self.table[self.i]]))  # 若均不符合，则引出异常

    def calculate(self, tokens=None, type='after'):
        if tokens == None:
            tokens = self.table
        if type == 'after':
            expression = self.middle_to_after(tokens[:-1])
        elif type == 'front':
            expression = self.middle_to_front(tokens[:-1])
        else:
            raise TypeError
        result = self.expression_to_value(expression, type)
        if self.is_assign:
            self.word_dict[self.key] = result
        return expression, result

    def middle_to_after(self, tokens):
        """中缀表达式变为后缀表达式"""
        expression = []  # s2
        ops = []  # s1
        for item in tokens:
            # 当遇到运算符
            if item in ['+', '-', '*', '/', "^", '%', '//']:
                while len(ops) >= 0:
                    # 如果栈中没有运算符，直接将运算符添加到后缀表达式
                    if len(ops) == 0:
                        ops.append(item)
                        break
                    # 如果栈中有运算符
                    op = ops.pop()
                    # 如果栈顶的运算符比当前运算符级别低，当前运算符入栈
                    if op == '(' or ops_rule[item] > ops_rule[op]:
                        ops.append(op)
                        ops.append(item)
                        break
                    else:
                        # 如果栈顶的运算符比当前运算符级别高，将栈顶运算符加入到表达式
                        # 当前运算符与栈中后面的运算符比较
                        expression.append(op)
            # 遇到左括号入栈
            elif item == '(':
                ops.append(item)
            # 遇到右括号，将栈中运算符加入到表达式直到遇到左括号
            elif item == ')':
                while len(ops) > 0:
                    op = ops.pop()
                    if op == '(':
                        break
                    else:
                        expression.append(op)
            # 遇到运算数，添加到表达式
            else:
                expression.append(item)
        # 最后将栈中全部运算符加到后缀表达式中
        while len(ops) > 0:
            expression.append(ops.pop())

        return expression

    def expression_to_value(self, expression, type='after'):
        """后缀表达式计算"""
        if type == 'after':
            stack_value = []
            for item in expression:
                if item in ['+', '-', '*', '/', '^', '%', '//']:
                    n2 = stack_value.pop()
                    n1 = stack_value.pop()
                    result = self.cal(n1, n2, item)
                    stack_value.append(result)
                else:
                    if self.dic[item] == 1:  # 为标识符
                        try:
                            item = self.word_dict[item]
                        except KeyError:
                            raise IndentiNotFountError(item)
                    stack_value.append(float(item))
            return stack_value[0]
        elif type == 'front':
            # expression.reverse()
            stack_value = []
            for item in expression[::-1]:
                if item in ['+', '-', '*', '/', '^', '%', '//']:
                    n1 = stack_value.pop()
                    n2 = stack_value.pop()
                    result = self.cal(n1, n2, item)
                    stack_value.append(result)
                else:
                    if self.dic[item] == 1:  # 为标识符
                        try:
                            item = self.word_dict[item]
                        except KeyError:
                            raise IndentiNotFountError(item)
                    stack_value.append(float(item))
            return stack_value[0]

    def middle_to_front(self, tokens):
        """中缀表达式变为前缀表达式"""
        expression = []  # s2
        ops = []  # s1
        # tokens.reverse()
        for item in tokens[::-1]:
            # 当遇到运算符
            if item in ['+', '-', '*', '/', "^", '%', '//']:
                while len(ops) >= 0:
                    # 如果栈中没有运算符，直接将运算符添加到前缀表达式
                    if len(ops) == 0:
                        ops.append(item)
                        break
                    # 如果栈中有运算符
                    op = ops.pop()
                    # 如果栈顶的运算符比当前运算符级别低，当前运算符入栈
                    if op == ')' or ops_rule[item] >= ops_rule[op]:
                        ops.append(op)
                        ops.append(item)
                        break
                    else:
                        # 如果栈顶的运算符比当前运算符级别高，将栈顶运算符加入到表达式
                        # 当前运算符与栈中后面的运算符比较
                        expression.append(op)
            # 遇到左括号入栈
            elif item == '(':
                while len(ops) > 0:
                    op = ops.pop()
                    if op == ')':
                        break
                    else:
                        expression.append(op)
            # 遇到右括号，将栈中运算符加入到表达式直到遇到左括号
            elif item == ')':
                ops.append(item)

            # 遇到运算数，添加到表达式
            else:
                expression.append(item)
        # 最后将栈中全部运算符加到后缀表达式中
        while len(ops) > 0:
            expression.append(ops.pop())

        return expression[::-1]

    # 计算函数
    def cal(self, n1, n2, op):
        if op == '+':
            return n1 + n2
        if op == '-':
            return n1 - n2
        if op == '*':
            return n1 * n2
        if op == '/':
            try:
                return n1 / n2
            except ZeroDivisionError:
                raise ZeroDivError
        if op == '^':
            return n1 ** n2
        if op == '%':
            return n1 % n2
        if op == '//':
            return n1 // n2


#######################################        主程序         #######################################
if __name__ == '__main__':
    # string = input('请输入表达式：')
    string = "aaa= 2+1"
    cal = Calculator()
    tokens = cal.cifa(string)
    # tokens = cal.cifa("b=a+1")
    wenfa = cal.yufa()
    expression, result = cal.calculate(type='front')
    # print(expression, result)
    # yuyi()
