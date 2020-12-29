class BaseError(Exception):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return ("位置{}，操作数定义错误，数字串中不能出现字母").format(self.position)


class PointError(BaseError):
    def __str__(self):
        return ("位置{}，小数点错误").format(self.position)


class ValueError(BaseError):
    def __str__(self):
        return ("位置{}，词法分析检测到非法字符").format(self.position)


class EOFError(BaseError):
    def __str__(self):
        return ("位置{}，语法分析程序检查到错误,'('前应该有运算符").format(self.position)


class CifaError(BaseError):
    def __init__(self, pos, dec):
        self.dec = dec
        self.position = pos

    def __str__(self):
        return ("位置{}，{}").format(self.position, self.dec)


class NumberError(BaseError):
    def __str__(self):
        return ("位置{}，词法分析错误，数字串中不能包含字母").format(self.position)


class InvalidCharError(BaseError):
    def __str__(self):
        return ("位置{}，词法分析错误，检测到非法字符".format(self.position))


class EqualSignError(BaseError):
    def __str__(self):
        return ("词法分析错误，‘=‘过多")


class IndentiNotFountError(BaseError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("标识符{}没有在单词表中".format(self.value))
