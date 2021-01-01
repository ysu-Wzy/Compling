class BaseError(Exception):
    def __init__(self, position=0, char=None):
        self.position = position+1
        self.char = char


class PointError(BaseError):
    def __str__(self):
        return ("词法分析出错，位置{}，小数点错误".format(self.position))


class YufaError(BaseError):
    def __init__(self,position=0,dec=""):
        self.position = position+1
        self.dec = dec
    def __str__(self):
        return ("语法分析出错，错误位置{},{}".format(self.position,self.dec))

class EOFError(BaseError):
    def __str__(self):
        return ("语法分析出错，位置{},括号不匹配").format(self.position)


class IdentifierDefineError(BaseError):
    def __str__(self):
        return ("词法分析出错，位置{}，标识符中必须由数字和字母组成，且必须以字母开头").format(self.position)


class NumberError(BaseError):
    def __str__(self):
        return ("词法分析出错，位置{}，数字串中不能包含字母 {}").format(self.position,self.char)


class InvalidCharError(BaseError):
    def __str__(self):
        return ("词法分析出错，位置{}，检测到非法字符：{}".format(self.position, self.char))


class EqualSignError(BaseError):
    def __str__(self):
        return ("词法分析错误，‘=‘过多")


class IndentiNotFountError(BaseError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("计算出错，标识符{}没有在单词表中".format(self.value))

class ZeroDivError(BaseError):
    def __str__(self):
        return ("除数不能为零")

