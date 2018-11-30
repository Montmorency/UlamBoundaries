import argparse 
import numpy as np

class Grid(object):
  def __init__(self, N):
  #Grid defined by linear array of blocks and its dimension
  #can return a block id in the linear array from its 
  #coordinate pair. Start from 0,0 corner.
    self.dim_x = N
    self.dim_y = N
    self.N = self.dim_x*self.dim_y
    self.blocks = []
    self.generation = 0
  #mortality constraint
    self.death_rule = 0

  def block_id(self, coords):
    #generate block id. For edge cases
    #return N which is beyond neighbour list.
    if (coords[0] < 0) or (coords[1] < 0):
      return self.N
    elif (coords[0] > (self.dim_x-1)) or (coords[1] > (self.dim_y-1)):
      return self.N
    else:
      return self.dim_x*(coords[1]) + coords[0]

  def set_neighbours(self, mode='rectangular'):
    """
    num sets the number of neighbours that need to be checked.
    The Ulam generation rules only apply to "contiguous" i.e.
    rectangularly displaced grids, but the rules apply to any
    squares that touch at a point.

    Possible neighbour modes are then: 
      rectangular:
        4 neighbouring grids along principle branch
        and stems.

      planar:
        8 neighbouring grids in the plane
    """
    for block in self.blocks:
        if mode =='rectangular':
          neighbour_pairs = [(block.x-1, block.y), (block.x+1, block.y),
                             (block.x, block.y-1), (block.x, block.y+1)]
        elif mode =='planar':
          neighbour_pairs = [(block.x-1, block.y), (block.x+1, block.y),
                             (block.x, block.y-1), (block.x, block.y+1),
                             (block.x-1, block.y-1), (block.x-1, block.y+1),
                             (block.x+1, block.y-1), (block.x+1, block.y+1)]
        else:
          raise("Neighbour mode not recognized.")
        neighbour_list = []
        for n_coord in neighbour_pairs:
          neighbour_id = self.block_id(n_coord)
          if 0 <= neighbour_id < self.N:
            neighbour_list.append(self.blocks[neighbour_id])
        #if mode == 'planar': print neighbour_list
        block.neighbours = neighbour_list

  def iterate(self):
    for block in self.blocks:
      if (block.state == 0) and (sum([n.state for n in block.neighbours]) == 1):
        block.tmp = 'p'
        block.age = 0
        parent = filter(lambda x: x.state ==1, block.neighbours)[0]
        block.parent =  parent
        block.grand_parent = parent.parent
      else:
        block.tmp = block.state
        block.age += 1

  def prune(self, mode='dense'):
    #go through blocks marked as potential.
    self.set_neighbours(mode='planar')
    for block in self.blocks:
      if mode == 'dense':
        if block.tmp == 'p':
          block.state = 1
        else:
          block.tmp = block.state
      elif mode == 'sparse':
        if block.tmp == 'p':
          for n in block.neighbours:
            if n.tmp=='p' and (n.parent != block.parent):
              block.state = 0
            else:
              block.state = 1

class Block(object):
  def __init__(self, x, y, state):
    self.state = state
    self.tmp = state
    self.coords = (x,y)
    self.x = x
    self.y = y
    #age of cell
    self.age = 0
    self.neighbours = []
    self.parent = None
    self.grand_parent = None

  def __repr__(self):
    return '({},{}) {} {}'.format(self.x, self.y, self.state, self.tmp)

# From article On Recursively Defined Geometrical Object and Patterns
# of Growth. See also March 1983 conference at Los Alamos and report
# written by Wolfram
# Rules are:
# A square of the next generation is formed if:
# a) it is contiguous to one and only one square of the current generation, and
# b) it touches no other previously occupied square except if the square should be its "grandparent." In addition:
# c) of this set of prospective squares of the (n+1)^{th} generation satisfying the previous condition,
#    we eliminate all squares that would touch each other. However, squares that have the same parent are
#    allowed to touch.
# Applications:
# Identifying Atavistic traits in Cellular Automata.
# Mapping different crystal growth patterns? 8 neighbours of BCC onto grid.
# Show the pattern of growth.

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", default='dense')
args = parser.parse_args()

N = 11
N_gens = 10

print '{0}x{0} grid '.format(N) 
print 'mode: ', args.mode

grid_array = np.zeros([N,N])
init_array = np.zeros([N,N])

#seed upper left
#init_array[0,0]=1
init_array[5,5] = 1

#Test Suite Self-Replicating States
#4x4 static
#init_array[0,1] = 1 
#init_array[0,2] = 1 
#init_array[1,0] = 1 
#init_array[1,3] = 1 
#init_array[2,0] = 1 
#init_array[2,3] = 1 
#init_array[3,1] = 1 
#init_array[3,2] = 1 
#5x5 static and its transpose.
#init_array[0,0] = 1 
#init_array[1,0] = 1 
#init_array[3,0] = 1 
#init_array[4,0] = 1 
#init_array[0,2] = 1 
#init_array[1,2] = 1 
#init_array[3,2] = 1 
#init_array[4,2] = 1 
#init_array[0,4] = 1 
#init_array[1,4] = 1 
#init_array[3,4] = 1 
#init_array[4,4] = 1 

grid = Grid(N)
grid.blocks = []
for y in range(N):
  for x in range(N):
    block = Block(x,y,init_array[x,y])
    grid.blocks.append(block)

print 'Generation 0'
print init_array

generation = 0
while generation <= N_gens:
  generation += 1
  grid.generation = generation
  grid.set_neighbours(mode='rectangular')
  grid.iterate()
  grid.prune(mode=args.mode)
#  grid.transition()
  for block in grid.blocks:
    grid_array[block.coords] = block.state
  print 'Generation: ', generation 
  print grid_array

