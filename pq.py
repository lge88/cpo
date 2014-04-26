class PQNode:
  def __init__(self, item, prior):
    self.item = item
    self.prior = prior

class MinPriorityQueue:
  def __init__(self):
    self._items = []

  def insert_with_priority(self, item, prior):
    node = PQNode(item, prior)

    self._items.append(node)
    self._items.sort(self.comp)

  def comp(self, node_1, node_2):
    if node_1.prior - node_2.prior > 0:
      return 1
    elif node_1.prior - node_2.prior < 0:
      return -1
    else:
      return 0

  def delMin(self):
    node = self._items.pop(0)
    return node.item

  def empty(self):
    return len(self._items) == 0


if __name__ == '__main__':
  # xvec = read_initial_input(filepath)

  pq = MinPriorityQueue()

  pq.insert_with_priority('A', 4.3)
  pq.insert_with_priority('B', 2.4)
  pq.insert_with_priority('C', 1.0)
  pq.insert_with_priority('D', 3.0)

  print pq.delMin() # C
  print pq.delMin() # B
  print pq.delMin() # D
  print pq.delMin() # A
