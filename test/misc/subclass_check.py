from common_utils.check_utils import check_type

class Test0:
    def __init__(self, a: int, b: int):
        check_type(a, valid_type_list=[int])
        check_type(b, valid_type_list=[int])
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, Test0):
            return self.a == other.a and self.b == other.b
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Test0):
            return Test1(a=self.a+other.a, b=self.b+other.b)
        else:
            raise Exception

class Test1(Test0):
    def __init__(self, a: int, b: int):
        super().__init__(a=a, b=b)
    
    def __eq__(self, other):
        if isinstance(other, Test1):
            return self.a == other.a and self.b == other.b
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Test1):
            return Test1(a=self.a+other.a, b=self.b+other.b)
        else:
            raise Exception
    
test0 = Test0(a=1, b=2)
test1 = Test1(a=3, b=4)

assert test0 + test1 == Test1(a=test0.a+test1.a, b=test0.b+test1.b)