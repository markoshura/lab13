class Matrix:
    def __init__(self, *ems):
        if len(ems) == 0: raise ValueError('Not enough parameters')
        if type(ems[0]) not in [list, tuple]:
            if len(ems) != 2:
                raise ValueError('Two parameters expected, {} given'.format(len(ems)))
            if not(type(ems[0])==type(ems[1])==int):
                raise ValueError('Ints expected')
            if not(ems[0]>0 and ems[1]>0): raise ValueError('Int error')
            self.w, self.h = ems
            self.__ems = [[0]*self.w for i in range(self.h)]
        else:
            ems=ems[0]
            if len(ems) == 0: raise ValueError('Cannot create matrix from an empty list')
            if not all(len(x) == len(ems[0]) for x in ems): raise ValueError('Input list rows have diffirent length')
            self.w, self.h = len(ems[0]), len(ems)
            self.__ems = [list(i) for i in ems]
    get_m = lambda self: self.w
    get_n = lambda self: self.h
    get_size = lambda self: (self.w, self.h)
    is_square = lambda self: self.w == self.h
    def invert(self):
        if not self.is_square(): raise ValueError('Can only invert a square matrix')
        if (self.w, self.h) == (2, 2):
            a, b, c, d = self.__ems[0] + self.__ems[1]
            det = a*d - b*c
            return Matrix(((d/det, -b/det), (-c/det, a/det)))
    def set(self,x, y, value):
        self.__ems[y][x] = value
    def get(self, x, y):
        return self.__ems[y][x]
    def transpose(self):
        return Matrix(list(zip(*self.__ems)))
    def __str__(self):
        return '\n'.join(['('+', '.join([str(self.__ems[i][j]) for j in range(self.w)])+')' for i in range(self.h)])
    def comparable(self, other):
        if type(other) != Matrix: raise ValueError('Can only compare matrixes, {} is a {}, not a matrix'.format(other, type(other)))
        return self.w == other.w and self.h == other.h
    def __eq__(self, other):
        if not self.comparable(other): raise ValueError('Cannot compare matrixes of diffirent size')
        return all(all(self.__ems[i][j]==other.__ems[i][j] for j in range(len(self.__ems[0]))) for i in range(len(self.__ems)))
    def __add__(self, other):
        if not self.comparable(other): raise ValueError('Cannot add matrixes of diffirent size')
        return Matrix([[self.__ems[i][j]+other.__ems[i][j] for j in range(len(self.__ems[0]))] for i in range(len(self.__ems))])
    def __sub__(self, other):
        if not self.comparable(other): raise ValueError('Нельзя вычитать матрицы разного размера')
        return Matrix([[self.__ems[i][j]-other.__ems[i][j] for j in range(len(self.__ems[0]))] for i in range(len(self.__ems))])
    def __cross(self, x, y):
        return Matrix([row[:x]+row[x+1:] for row in self.__ems[:y] + self.__ems[y+1:]])
    def __mul__(self, other):
        if type(other) not in [int, float, Matrix]: raise ValueError('Cannot multiply matrix and', type(other))
        if type(other) == Matrix:
            other, self = self, other #A terrible crutch, I know
            if self.w != other.h: raise ValueError('Matrixes cannot be multiplied')
            return Matrix([[sum(row1[i]*other.__ems[i][col2_ind] for i in range(self.w)) for col2_ind in range(other.w)] for row1 in self.__ems])
        else:
            return Matrix([[self.__ems[i][j]*other for j in range(self.w)] for i in range(self.h)])
    def __truediv__(self, other):
        if type(other) in [int, float]:
            return self * (1/other)
        else:
            raise ValueError()
    def determinant(self):
        if not self.is_square(): raise ValueError('Not a square matrix!')
        if self.w == 1: return self.__ems[0][0]
        else:
            return sum([(-1)**i * self.__ems[0][i] * self.__cross(i, 0).determinant() for i in range(self.w)])
