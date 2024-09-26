import numpy as np
from dataclasses import dataclass


@dataclass(init=True, frozen=True) 
class Vec2:

    _r: float | None = None  # Radial distance (if polar)
    _theta: float | None = None  # Angle in radians (if polar)
    data: np.ndarray = None  # Cartesian (x, y) representation
    _polar: bool = False

    def __init__(self, v1=0.0, v2=0.0, polar=False):
        object.__setattr__(self, '_polar', polar)
        if self._polar:
            # If initialized in polar coordinates, store both polar and Cartesian values
            object.__setattr__(self, '_r', v1)
            object.__setattr__(self, '_theta', v2)
            x = v1 * np.cos(v2)
            y = v1 * np.sin(v2)
        else:
            x = v1
            y = v2

        object.__setattr__(self, 'data', np.array([x, y], dtype=float))

    
    def isPolar(self):
        return self._polar
    
    # Convert to polar coordinates, but only if initialized in polar coordinates
    def polar(self):
        """
        Return the polar coordinates (r, theta).
        """
        if self.isPolar() and (self._r is not None and self._theta is not None):
            return self._r, self._theta
        else:
            # If the vector was initialized in Cartesian coordinates and polar not available
            raise ValueError("Polar coordinates were not provided at initialization.")

    # Representation of the vector
    def __repr__(self):
        return f"Vec2({self.data[0]}, {self.data[1]})"

    # Overload the string method for easy printing
    def __str__(self):
        return f"({self.data[0]}, {self.data[1]})"

    # Get the length of the vector (Euclidean norm)
    def norm(self):
        return np.linalg.norm(self.data)

    # Addition overload
    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(*(self.data + other.data))
        else:
            return Vec2(*(self.data + other))

    # Subtraction overload
    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(*(self.data - other.data))
        else:
            return Vec2(*(self.data - other))

    # Multiplication overload (scalar)
    def __mul__(self, scalar):
        return Vec2(*(self.data * scalar))

    # Division overload (scalar)
    def __truediv__(self, scalar):
        return Vec2(*(self.data / scalar))

    # Negation overload
    def __neg__(self):
        return Vec2(*(-self.data))

    # Equality overload
    def __eq__(self, other):
        return np.allclose(self.data, other.data)

    # Dot product overload
    def dot(self, other):
        if isinstance(other, Vec2):
            return np.dot(self.data, other.data)
        else:
            raise ValueError("Dot product requires another Vec2 object")

    # Overloading the @ operator for dot product
    def __matmul__(self, other):
        return self.dot(other)

    # Cross product (2D cross product returns a scalar)
    def cross(self, other):
        if isinstance(other, Vec2):
            return np.cross(self.data, other.data)
        else:
            raise ValueError("Cross product requires another Vec2 object")

    # Indexing support to access components like an array
    def __getitem__(self, index):
        return self.data[index]

    # Set items like an array
    def __setitem__(self, index, value):
        self.data[index] = value

    # Overload abs() to return the length of the vector
    def __abs__(self):
        return self.norm()

    # Overload len() to return the number of elements (2 for Vec2)
    def __len__(self):
        return 2


class VelVec2(Vec2):
    def __init__(self, v1, v2, polar = False):
        super().__init__(v1, v2, polar)

    def rdot(self):
        if self.isPolar() and (self._r is not None and self._theta is not None): 
            return self._r
        else:
            # If the vector was initialized in Cartesian coordinates and polar not available
            raise ValueError("Polar coordinates were not provided at initialization.")

    def rthetadot(self):
        if self.isPolar() and (self._r is not None and self._theta is not None):
            return self._theta
        else:
            raise ValueError("Polar coordinates were not provided at initialization.")

    def thetadot(self, r : Vec2):
        if self.isPolar() and (self._r is not None and self._theta is not None):
            if(r.norm == 0):
                raise ZeroDivisionError('As r = 0, thetadot can\'t be provided')

            return self._theta / r.norm() 
        else:
            raise ValueError("Polar coordinates were not provided at initialization.")
        

def Vec2Polar(r: float = 0.0, theta: float = 0.0) -> Vec2:
    return Vec2(r, theta, polar = True)

def VelVec2Polar(rdot: float = 0.0, thetadot: float = 0.0) -> VelVec2:
    return VelVec2(rdot, thetadot, polar = True)


r = Vec2Polar(10,10)
v = VelVec2Polar(10,13)

print(v.thetadot(r))
