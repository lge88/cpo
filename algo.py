from subprocess import Popen, PIPE, STDOUT
import operator
from random import random
from math import sqrt

from kcube import KCube
from pq import MinPriorityQueue

filepath = 'input.txt'
prog = ['tclsh', 'f.tcl']


def read_initial_input(filepath):
  with open(filepath) as f:
    lines = f.readlines()
  return [float(line.strip()) for line in lines]

def eval_fun(xvec):
  p = Popen(prog, stdout = PIPE, stdin = PIPE)

  lines = ''.join([str(x) + '\n' for x in xvec])
  out = p.communicate(input = lines)[0]

  return float(out)

def get_refine_vector(f, cube):
  d = cube.dim()
  return [0.5 for x in range(d)]

def get_xs_key(xvec):
  return '_'.join([str(x) for x in xvec])

def eval_fun_for_vertices(f, vertices, memo):
  ys = []
  for vert in vertices:
    xs_key = get_xs_key(vert)
    if not memo.has_key(xs_key):
      y = f(vert)
      memo[xs_key] = (y,) + vert

    y = memo[xs_key][0]
    ys.append(y)

  return ys

def is_colinear(p1, p0, p2, tol = 1e-2):
  x1, y1 = p1
  x2, y2 = p2
  x0, y0 = p0
  d = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1))/sqrt((x2-x1)**2+(y2-y1)**2)
  dist_p1_p2 = sqrt((x2 - x1) **2 + (y2 - y1) **2)
  ratio = d / dist_p1_p2

  res = ratio < tol
  return res

def is_on_plane(p1, p2, p3, p4, tol = 1e5):
  x1, y1, z1 = p1
  x2, y2, z2 = p2
  x3, y3, z3 = p3
  x4, y4, z4 = p4

  det = x1*y2*z3 - x1*y3*z2 - x2*y1*z3 + x2*y3*z1 + \
      x3*y1*z2 - x3*y2*z1 - x1*y2*z4 + x1*y4*z2 + \
      x2*y1*z4 - x2*y4*z1 - x4*y1*z2 + x4*y2*z1 + \
      x1*y3*z4 - x1*y4*z3 - x3*y1*z4 + x3*y4*z1 + \
      x4*y1*z3 - x4*y3*z1 - x2*y3*z4 + x2*y4*z3 + \
      x3*y2*z4 - x3*y4*z2 - x4*y2*z3 + x4*y3*z2

  res =  abs(det) < tol
  print res
  return res

def aver_4_3dvec(xvec1, xvec2, xvec3, xvec4):
  x = 0.25 * (xvec1[0] + xvec2[0] + xvec3[0] + xvec4[0])
  y = 0.25 * (xvec1[1] + xvec2[1] + xvec3[1] + xvec4[1])
  z = 0.25 * (xvec1[2] + xvec2[2] + xvec3[2] + xvec4[2])
  return (x, y, z)

# [(0, 1), (0, 1)], d=1 =>
#    [(0.5, 0), (0.5, 0.5), (0.5, 1)]
# [(0, 1), (0, 1), (0, 2)], d=1
#    => [(0.5, 0, 1), (0.5, 0.5, 1), (0.5, 1, 1)]
def get_3pts_at_dim(cube, d):
  bounds = cube._bounds
  mids = [0.5*(low+high) for low, high in bounds]

  p1 = list(mids)
  p1[d] = bounds[d][0]

  p2 = list(mids)

  p3 = list(mids)
  p3[d] = bounds[d][1]

  return tuple([tuple(p) for p in [p1, p2, p3]])


def maybe_refine(f, cube):
  vertices = cube.vertices()

  num_of_dims = cube.dim()
  refine_vec = []

  for d in range(num_of_dims):
    p1, p2, p3 = get_3pts_at_dim(cube, d)

    x1 = p1[d]
    x2 = p2[d]
    x3 = p3[d]

    y1 = f(p1)
    y2 = f(p2)
    y3 = f(p3)

    hp1 = (x1, y1)
    hp2 = (x2, y2)
    hp3 = (x3, y3)

    if is_colinear(hp1, hp2, hp3):
      refine_vec.append(None)
    else:
      refine_vec.append(0.5)

  new_cubes = cube.subdivide(refine_vec)
  return new_cubes

def algo(f, cubes, max_iter = 5):
  # q = MinPriorityQueue()
  q = Queue()

  seen_cubes = {}
  memo = {}

  y_min = float('inf')
  xvec_at_y_min = None

  # Init with random priority:
  for cube in cubes:
    cube_tag = cube.get_tag()
    seen_cubes[cube_tag] = True

    vertices = cube.vertices()
    ys = eval_fun_for_vertices(f, vertices, memo)

    y_min_index, y_min_value = min(enumerate(ys), key=operator.itemgetter(1))
    y_avg = sum(ys) / len(ys)

    if y_min_value < y_min:
      y_min = y_min_value
      xvec_at_y_min = vertices[y_min_index]

    # q.insert_with_priority(cube, y_avg)
    q.enqueue(cube)

  i = 0
  while not q.empty() and i < max_iter:
    # cube = q.delMin()
    cube = q.dequeue()

    new_cubes = maybe_refine(f, cube)

    for new_cube in new_cubes:

      new_cube_tag = new_cube.get_tag()
      if seen_cubes.has_key(new_cube_tag): continue

      seen_cubes[new_cube_tag] = True

      vertices = new_cube.vertices()
      ys = eval_fun_for_vertices(f, vertices, memo)

      y_min_index, y_min_value = min(enumerate(ys), key=operator.itemgetter(1))
      y_avg = sum(ys) / len(ys)

      if y_min_value < y_min:
        y_min = y_min_value
        xvec_at_y_min = vertices[y_min_index]

      # q.insert_with_priority(new_cube, y_avg)
      q.enqueue(new_cube)

    i = i + 1

  return (memo.values(), y_min, xvec_at_y_min)



class Stack:
  def __init__(self, items):
    self._items = list(items)

  def push(self, item):
    self._items.append(item)

  def pop(self):
    return self._items.pop()

  def empty(self):
    return len(self._items) == 0

class Queue:
  def __init__(self, items = []):
    self._items = list(items)

  def enqueue(self, item):
    self._items.append(item)

  def dequeue(self):
    return self._items.pop(0)

  def empty(self):
    return len(self._items) == 0

if __name__ == '__main__':

  cubes0 = KCube([(-1, 1), (-1, 1)]).subdivide([0.5, 0.5])

  vals, ymin, xatymin = algo(eval_fun, cubes0)

  print vals
  print ymin
  print xatymin
