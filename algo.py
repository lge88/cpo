from kcube import *
from subprocess import Popen, PIPE, STDOUT

filepath = 'input.txt'
prog = ['tclsh', 'f.tcl']


def read_initial_input(filepath):
  with open(filepath) as f:
    lines = f.readlines()
  return [float(line.strip()) for line in lines]

def eval_fun(xvec):
  p = Popen(prog, stdout = PIPE, stdin = PIPE)

  lines = ''.join([str(x) + '\n' for x in xvec])
  out = p.communicate(input=lines)[0]

  return float(out)

def get_refine_vector(cube, ys, criteria=None):
  d = cube.dim()
  return [0.5 for x in range(d)]

def get_xs_key(xvec):
  return '_'.join([str(x) for x in xvec])

def algo(f, cubes, max_iter = 5):
  i = 0
  s = Queue(cubes)
  seen_cubes = {}
  table_xvec_to_y = {}

  y_min = float('inf')
  xvec_at_y_min = None

  while not s.empty() and i < max_iter:
    c = s.dequeue()
    seen_cubes[c.get_tag()] = True

    xs = c.vertices()
    ys = []

    for xvec in xs:
      xs_key = get_xs_key(xvec)
      if not table_xvec_to_y.has_key(xs_key):
        y = f(xvec)
        table_xvec_to_y[xs_key] = y

      y = table_xvec_to_y[xs_key]

      if y < y_min:
        y_min = y
        xvec_at_y_min = xvec

      ys.append(y)

    refine_vec = get_refine_vector(c, ys)

    for nc in c.subdivide(refine_vec):
      nc_tag = nc.get_tag()
      if not seen_cubes.has_key(nc_tag):
        s.enqueue(nc)

    i = i + 1

  return (table_xvec_to_y, y_min, xvec_at_y_min)

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
  # xvec = read_initial_input(filepath)

  cubes0 = KCube([(-1, 1), (-1, 1)]).subdivide([0.5, 0.5])

  tb, ymin, xatymin = algo(eval_fun, cubes0)

  print tb
  print ymin
  print xatymin
