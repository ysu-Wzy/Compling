# -*- coding=utf-8 -*-
# PYTHON实现算术表达式的词法语法语义分析（编译原理应用）
# https://blog.csdn.net/QFire/article/details/81236928
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
    '^': 3
}
###################################        语法分析         #####################################
'''
基本文法：
M -> +E|-E|E
E -> TE~
E~ -> +TE~|-TE~|&
T -> FT~
T~ -> *FT~|/FT~|&|^FT~|%FT~
F -> (E)|indentifer|digit|-indentifer
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

    #####################################        词法分析        ######################################
    def cifa(self, string):  # 词法分析
        self.table = []
        print('')
        m = 0
        point = False  # 是否允许出现小数点
        state = None  # 1：为标识符 2：为数字串 3：为运算符
        for i in range(len(string)):
            # if string[i]!="-":
            if string[i] in operator_list:  # 如果是运算符
                if state == identifier:  # state=1表明其前面的为标识符
                    print(string[m:i], '是标识符,类型码：1')
                    self.dic[string[m:i]] = identifier
                    self.table.append(string[m:i])
                elif state == digit:  # state=2表明其前面的为数字
                    print(string[m:i], '是数字，类型码：2')
                    self.dic[string[m:i]] = digit
                    self.table.append(string[m:i])
                    point = False
                m = i + 1
                state = operator
                print(string[i], '是运算符，类型码：3')
                self.dic[string[i]] = operator
                self.table.append(string[i])
            elif string[i] in number:  # 如果是数字
                # if string[i] == '.':
                #     point = False
                if i == m:  # 是数字的第一个字符
                    point = True
                    state = digit
            elif string[i] in letter:  # 如果是字母
                if state == digit:  # 判断此时的状态，若state=2表明状态为无符号整数，而整数内不能包含字母，故报错
                    print('词法分析检测到错误,数字串中不能包含字母')
                    return '词法分析检测到错误,数字串中不能包含字母'
                if i == m:  # 判断此时的字母是否为标识符的第一个字母，若是则改变状态为标识符
                    state = identifier
                    point = False
            elif string[i] == '.':
                if point == True:
                    continue
                else:
                    print("小数点错误")
                    return "小数点错误"
            else:  # 当输入的字符均不符合以上判断，则说明为非法字符，故报错
                print('词法分析检测到非法字符')
                return "词法分析检测到非法字符"

        if state == identifier:  # 当字符串检查完后，若字符串最后部分为标识符，应将其print出来
            print(string[m:], '是标识符，类型码：3')
            self.dic[string[m:]] = identifier
            self.table.append(string[m:])
        elif state == digit:  # 若字符串最后部分为无符号整数，应将其print出来
            print(string[m:], '是无符号整数，类型码：2')
            self.dic[string[m:]] = digit
            self.table.append(string[m:])
        self.table.append('#')
        print('字符栈:', self.table, '\n词法正确')
        return self.table #+ ["#"]

    def yufa(self):
        self.i = 0  # 指针归零
        self.wenfa = []
        try:  # 用异常处理程序捕获程序的错误，出现异常则报错
            self.m()
            return self.wenfa
        except:
            print('\n语法分析程序检查到错误,位置%s' % self.i)
            return '\n语法分析程序检查到错误,位置%s' % self.i

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
            return "\n语法分析程序检查到错误,'('前应该有运算符"
        else:
            print('\n字符串语法是：')  # 若一切正确，则输出语法树文法
            for i in self.wenfa:
                print(i)
            print('语法正确')

    def e(self):  # PE程序
        self.wenfa.append('E -> TE1')
        self.t()
        self.e1()

    def e1(self):  # PE1程序
        if (self.table[self.i] == '+'):
            self.i += 1
            self.wenfa.append('E1 -> +TE1')
            self.t()
            self.e1()
        elif (self.table[self.i] == '-'):
            self.i += 1
            self.wenfa.append('E1 -> -TE1')
            self.t()
            self.e1()
        else:
            self.wenfa.append('E1 -> &')

    def t(self):  # PT程序
        self.wenfa.append('T -> FT1')
        self.f()
        self.t1()

    def t1(self):  # PT1程序
        if (self.table[self.i] == '*'):
            self.i += 1
            self.wenfa.append('T1 -> *FT1')
            self.f()
            self.t1()
        elif (self.table[self.i] == '/'):
            self.i += 1
            self.wenfa.append('T1 -> /FT1')
            self.f()
            self.t1()
        elif (self.table[self.i] == '^'):
            self.i += 1
            self.wenfa.append('T1 -> ^FT1')
            self.f()
            self.t1()
        elif (self.table[self.i] == '%'):
            self.i += 1
            self.wenfa.append('T1 -> %FT1')
            self.f()
            self.t1()
        else:
            self.wenfa.append('T1 -> &')

    def f(self):  # PF程序
        if (self.table[self.i] == '('):
            self.wenfa.append('F -> (E)')
            self.i += 1
            self.e()
            if (self.table[self.i] != ')'):
                raise Exception
            self.i += 1
        elif (self.dic[self.table[self.i]] == identifier):
            self.wenfa.append('F -> identifier ' + str(self.table[self.i]))
            self.i += 1
        elif (self.dic[self.table[self.i]] == digit):
            self.wenfa.append('F -> Digit ' + str(self.table[self.i]))
            self.i += 1
        elif (self.table[self.i] == '-'):
            self.wenfa.append('F ->  Digit ' + str(self.table[self.i]))
            self.i += 1
            if (self.dic[self.table[self.i]] == identifier):
                self.wenfa.append('F -> -identifier ' + str(self.table[self.i]))
                self.i += 1
            elif (self.dic[self.table[self.i]] == digit):
                self.wenfa.append('F -> -Digit ' + str(self.table[self.i]))
                self.i += 1
        else:
            raise Exception  # 若均不符合，则引出异常

    def calculate(self, type='after'):
        if type == 'after':
            expression = self.middle_to_after(self.table[:-1])
            return expression, self.expression_to_value(expression, type)
        elif type == 'front':
            expression = self.middle_to_front(self.table[:-1])
            return expression, self.expression_to_value(expression, type)
        else:
            raise TypeError

    def middle_to_after(self, tokens):
        """中缀表达式变为后缀表达式"""
        expression = []  # s2
        ops = []  # s1
        for item in tokens:
            # 当遇到运算符
            if item in ['+', '-', '*', '/', "^", '%']:
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
                if item in ['+', '-', '*', '/', '^', '%']:
                    n2 = stack_value.pop()
                    n1 = stack_value.pop()
                    result = self.cal(n1, n2, item)
                    stack_value.append(result)
                else:
                    stack_value.append(float(item))
            return stack_value[0]
        elif type == 'front':
            # expression.reverse()
            stack_value = []
            for item in expression[::-1]:
                if item in ['+', '-', '*', '/', '^', '%']:
                    n1 = stack_value.pop()
                    n2 = stack_value.pop()
                    result = self.cal(n1, n2, item)
                    stack_value.append(result)
                else:
                    stack_value.append(float(item))
            return stack_value[0]

    def middle_to_front(self, tokens):
        """中缀表达式变为前缀表达式"""
        expression = []  # s2
        ops = []  # s1
        # tokens.reverse()
        for item in tokens[::-1]:
            # 当遇到运算符
            if item in ['+', '-', '*', '/', "^", '%']:
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
        # tokens.reverse()
        # expression.reverse()
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
            return n1 // n2
        if op == '^':
            return n1 ** n2
        if op == '%':
            return n1 % n2


#######################################        主程序         #######################################
if __name__ == '__main__':
    # string = input('请输入表达式：')
    string = "1+((2+3)*4)+(-5)"
    cal = Calculator()
    tokens = cal.cifa(string)
    wenfa = cal.yufa()
    expression, result = cal.calculate('front')
    print(expression, result)
    # yuyi()
