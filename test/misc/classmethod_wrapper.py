from functools import wraps

class DecoratorCollection:
    def __init__(self, name: str):
        self.name = name

    def a(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f'This is method a. Made from collection: {self.name}')
            f(*args, **kwargs)
        return wrapper
    
    def b(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f'This is method b. Made from collection: {self.name}')
            f(*args, **kwargs)
        return wrapper
    
    def example(self, text: str):
        @self.a
        def func():
            print(f'This is an example. {text}')
        func()

dc = DecoratorCollection(name='MyCollection')

@dc.a
def test_x(x: int):
    print(f'x={x}')

@dc.b
def test_y(y: int):
    print(f'y={y}')

test_x(x=12)
test_y(y=20)
dc.example(text='Example Test')