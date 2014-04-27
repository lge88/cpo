from subprocess import Popen, PIPE, STDOUT
import operator

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

def algo(f, cubes, max_iter = 5):
  i = 0
  q = MinPriorityQueue()

  seen_cubes = {}
  memo = {}

  y_min = float('inf')
  xvec_at_y_min = None

  j = 0
  for cube in cubes:
    q.insert_with_priority(cube, j)
    seen_cubes[cube.get_tag()] = True
    j += 1

  while not q.empty() and i < max_iter:
    cube = q.delMin()

    refine_vec = get_refine_vector(f, cube)
    new_cubes = cube.subdivide(refine_vec)

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

      q.insert_with_priority(new_cube, y_avg)

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
  def __init__(self, items):
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
