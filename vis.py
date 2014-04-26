from kcube import *
from algo import *

if __name__ == '__main__':

  cubes0 = KCube([(-1, 1), (-1, 1)]).subdivide([None, None])

  vals, ymin, xatymin = algo(eval_fun, cubes0, 10)

  x1s = [t[1] for t in vals]
  x2s = [t[2] for t in vals]
  ys = [t[0] for t in vals]
  # scatter(x1s, x2s, c=ys)
