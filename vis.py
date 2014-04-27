from kcube import KCube
from algo import *
from pylab import *

if __name__ == '__main__':

  # cubes0 = KCube([(-10, 10)]).subdivide([None])
  cubes0 = KCube([(-10, 10), (-10, 10)]).subdivide([0.5, 0.5])

  vals, ymin, xatymin = algo(eval_fun, cubes0, 200)

  x1s = [t[1] for t in vals]
  x2s = [t[2] for t in vals]
  ys = [t[0] for t in vals]

  # scatter(x1s, ys)
  scatter(x1s, x2s, c=ys)
  show()
