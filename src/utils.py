import numpy as np


class Vec2:
    def __init__(self, v1=0.0, v2=0.0, polar=False):
        if polar:
            x = v1 * np.cos(v2)
            y = v1 * np.sin(v2)
        else:
            x = v1
            y = v2
            
        self.data = np.array([x, y], dtype=float)

    # Convert to polar coordinates
    def polar(self):
        """
        Converts Cartesian coordinates to polar coordinates.
        
        Returns:
        (r, theta): Tuple of radial distance and angle in radians.
        """
        x, y = self.data
        r = np.sqrt(x**2 + y**2)        # Radial distance
        theta = np.arctan2(y, x)        # Angle in radians
        return r, theta

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
        return self.length()

    # Overload len() to return the number of elements (2 for Vec2)
    def __len__(self):
        return 2


def Vec2Polar(r: float = 0.0, theta: float = 0.0) -> Vec2:
    return Vec2(r, theta, polar = True)
