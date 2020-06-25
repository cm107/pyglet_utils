class BasicObject:
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def position(self) -> (int, int):
        return (self.x, self.y)
    
    @position.setter
    def position(self, position: (int, int)):
        (self._x, self._y) = position

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, width: int):
        self._width = width
    
    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def shape(self) -> (int, int):
        return (self.width, self.height)
    
    @shape.setter
    def shape(self, shape: (int, int)):
        (self._width, self._height) = shape