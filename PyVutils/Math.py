# -*- coding: utf-8 -*-

# Vutils for Math

import math
import numpy as np
from enum import Enum

# ---

# 2D

def point_to_index_2d(p, ncol):
	x, y = p
	return y + x * ncol

def index_to_point_2d(index, ncol):
	x, y = divmod(index, ncol)
	return (x, y)

# 3D

def index_to_point_3d(index, nrow, ncol):
	z, _ = divmod(index, nrow * ncol)
	x, y = divmod(_, ncol)
	return (x, y, z)

def point_to_index_3d(p, nrow, ncol):
	x, y, z = p
	return y + x * ncol + z * nrow * ncol

# ---

def linear_regression(xs, ys):

    # Fx  = βx + α
    # Fx  = βx                                                   # suppose α = 0 for simplicity
    # J   = ∑(F𝗑ᵢ - yᵢ)² = ∑((α + β*xᵢ) - yᵢ)²                   # the function J called the cost/lost function
    # J   = ∑(F𝗑ᵢ - yᵢ)² = ∑(βxᵢ - yᵢ)² = ∑(β²xᵢ² - 2βxᵢyᵢ - y²)
    # J'  = ∑(2βxᵢ² - 2xᵢyᵢ) = ∑2βxᵢ² - ∑2xᵢyᵢ                   # derivatives J to find the slope
    # ½J' = ∑βxᵢ² - ∑xᵢyᵢ
    # ½J' = 0 <=> ∑βxᵢ² - ∑xᵢyᵢ = 0                              # finding the slope of J
    # β   = ∑xᵢyᵢ ÷ ∑xᵢ²
    # α   = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    num_pairs = min(np.size(xs), np.size(ys)) # pairs of data

    mean_x, mean_y = np.mean(xs), np.mean(ys)

    total_xy = total_xx = 0.

    for i in range(0, num_pairs):
        total_xy += (xs[i] - mean_x) * (ys[i] - mean_y)  # ∑xᵢyᵢ
        total_xx += (xs[i] - mean_x) * (xs[i] - mean_x)  # ∑xᵢ²
    pass

    b = total_xy / total_xx   # β = ∑xᵢyᵢ ÷ ∑xᵢ²
    a = mean_y - b * mean_x   # α = Fxᵢ - βxᵢ (xᵢ & yᵢ here are mean of x & y)

    return (a, b) # α & β

def find_representative_value_for_list_values(values: list, noise_filter: int = 1):
    '''
    Use the RANSAC regression to find the representative value of a list of values.
    :param values: A list of values
    :param noise_filter: The noise filter value
    :return: The representative value
    '''

    from sklearn.linear_model import RANSACRegressor

    Ys = [v // noise_filter * noise_filter for v in values]
    Xs = np.linspace(start=0, stop=10, num=len(Ys))

    _Xs = np.array(Xs).reshape(-1, 1)
    _Ys = np.array(Ys).reshape(-1, 1)

    ransac = RANSACRegressor()
    ransac.fit(_Xs, _Ys)

    # print(ransac.estimator_.coef_, ransac.estimator_.intercept_)
    # plt.plot(_Xs, ransac.predict(_Xs))
    # plt.plot(_Xs, _Ys)
    # plt.show()

    return ransac.estimator_.intercept_[0]

# Data Types

class AngleUnit(Enum):
  RAD = 0
  DEG = 1

class ValueType(Enum):
  Float = 1
  Integer = 2

ValueTypeMapping = {
  ValueType.Float: float,
  ValueType.Integer: int,
}

# Point

class Point:
  '''The class for point object
  Point(point)
  Point(x, y)
  Point(x, y, z)
  '''

  x = 0
  y = 0
  z = 0

  def __init__(self, *args):
    len_args = len(args)
    if len_args == 1: # point
      point  = args[0]
      self.x = point.x
      self.y = point.y
      self.z = point.z
    elif len_args == 2:  # Point2D(x, y)
      x, y, z, = *args, 0
      self.x = x
      self.y = y
      self.z = z
    elif len_args == 3:  # Point(x, y, z)
      x, y, z, = args
      self.x = x
      self.y = y
      self.z = z

  def __repr__(self):
    return f"Point({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

  def __add__(self, point): # point: Point
    return Vector(self.x + point.x, self.y + point.y, self.z + point.z)

  def __iadd__(self, point): # point: Point
    self.x += point.x
    self.y += point.y
    self.z += point.z
    return self

  def __sub__(self, point): # point: Point
    return Vector(self.x - point.x, self.y - point.y, self.z - point.z)

  def __isub__(self, point): # point: Point
    self.x -= point.x
    self.y -= point.y
    self.z -= point.z
    return self

  def __mul__(self, value: int or float):
    return Vector(self.x * value, self.y * value, self.z * value)

  def __imul__(self, value: int or float):
    self.x *= value
    self.y *= value
    self.z *= value
    return self

  def __div__(self, value: int or float):
    return Vector(self.x / value, self.y / value, self.z / value)

  def __idiv__(self, value: int or float):
    self.x /= value
    self.y /= value
    self.z /= value
    return self

  def to_list(self, type: ValueType = None) -> list:
    if type is None:
      return [self.x, self.y, self.z]
    else:
      T = ValueTypeMapping.get(type)
      return [T(self.x), T(self.y), T(self.z)]

  def to_tuple(self, type: ValueType = None) -> tuple:
    if type is None:
      return (self.x, self.y, self.z)
    else:
      T = ValueTypeMapping.get(type)
      return (T(self.x), T(self.y), T(self.z))

  def distance_to(self, point) -> float:
    return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2 + (self.z - point.z)**2)

# Point2D

class Point2D(Point):
  '''The class for point-2d object
  Point2D(Point)
  Point2D(x, y)
  '''
  def __init__(self, *args):
    super(Point2D, self).__init__(*args)
    self.z = 0

  def __repr__(self):
    return f"Point2D({self.x:.3f}, {self.y:.3f})"

  def to_list(self, type: ValueType = None) -> list:
    if type is None:
      return [self.x, self.y]
    else:
      T = ValueTypeMapping.get(type)
      return [T(self.x), T(self.y)]

  def to_tuple(self, type: ValueType = None) -> tuple:
    if type is None:
      return (self.x, self.y)
    else:
      T = ValueTypeMapping.get(type)
      return (T(self.x), T(self.y))

# Point3D

class Point3D(Point):
  '''The class for point-3d object
  Point3D(point)
  Point3D(x, y, z)
  '''
  def __init__(self, *args):
    super(Point3D, self).__init__(*args)

  def __repr__(self):
    return f"Point3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

# Vector

class Vector(Point):
  '''The class for vector object
  '''
  def __init__(self, *args):
    super(Vector, self).__init__(*args)

  def __repr__(self):
    return f"Vector({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

  def normalize(self):
    d = self.length()
    self.x /= d
    self.y /= d
    self.z /= d

  def length(self) -> float:
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)

  def dot(self, vec) -> float:
    return self.x * vec.x + self.y * vec.y + self.z * vec.z

  def angle_between(self, vec, unit=AngleUnit.DEG) -> float:
    a = math.acos(self.dot(vec) / (self.length() * vec.length()))
    if unit == AngleUnit.DEG: a = math.degrees(a)
    return a
