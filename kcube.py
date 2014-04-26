
class KCube:
  def __init__(self, bounds = []):
    self._bounds = list(bounds)

  def get_tag(self):
    return '_'.join([str(b[0]) + '_' + str(b[1]) for b in self._bounds])

  def __str__(self):
    return self._bounds.__str__()

  def subdivide(self, list_of_ratios):
    """
    If ratio is in (0, 1), subdivide the dimension;
    Else leave that dimension not divided.
    """
    if self.dim() <= 0: return [KCube()]

    lower_dim_cube = self.drop_first_dim()
    lower_dim_subs = lower_dim_cube.subdivide(list_of_ratios[1:])

    r = list_of_ratios[0]
    if r is None:
      return [c.prepend_dim(self._bounds[0]) for c in lower_dim_subs]
    else:
      low, high = self._bounds[0]
      stop = low + (high - low) * float(r)
      return [c.prepend_dim((low, stop)) for c in lower_dim_subs] + \
          [c.prepend_dim((stop, high)) for c in lower_dim_subs]

  def clone(self):
    return KCube(self._bounds)

  def prepend_dim(self, bound):
    res = self.clone()
    res._bounds = [bound] + res._bounds
    return res

  def drop_first_dim(self):
    res = self.clone()
    res._bounds = res._bounds[1:]
    return res

  def dim(self):
    return len(self._bounds)

  def vertices(self):
    if self.dim() <= 0: return [()]

    lower_dim_cube = KCube(self._bounds[1:])
    lower_dim_vertices = lower_dim_cube.vertices()

    return [(self._bounds[0][0],) + v for v in lower_dim_vertices] + \
        [(self._bounds[0][1],) + v for v in lower_dim_vertices]

if __name__ == '__main__':
  cube = KCube([(0, 1), (0, 1)])

  print cube
  print cube.vertices()
  print cube.get_tag()

  cubes = cube.subdivide([None, 0.5])

  i = 0
  for c in cubes:
    print 'c', i, ' veritces: ', c.vertices()
    print c.get_tag()
    i += 1
