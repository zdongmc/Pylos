import math
import uuid
import copy
import hashlib
import json

N = 3
COUNT_TOTAL = sum([ii*ii for ii in range(1, N+1)])
B, R, E = "B","R", " " # aliases of colors
CP, CN, CR, CL =  "CP", "CN", "CR", "CL" # alias of outcome classes
OC_DICT = json.load(open('oc_dict.json')) # maps state's id to its computed outcome_class

class State(object):
  """State of the game"""

  def __init__(self):
    # Unique ID
    self.outcome_class = None
    
    # Represent the game board as a nested dict of tuples
    self.board = {}
    for layer in range(N):
      self.board[layer] = {} 
      for row in range(layer+1):
        self.board[layer][row] = {}
        for col in range(layer+1):
          # Each location contains a tuple (color, availability)
          # - color: R/B/E
          # At init, everything is empty
          self.board[layer][row][col] = E
          
      # Define the player reserves
      self.count = {
        R: math.ceil(COUNT_TOTAL/2),
        B: math.ceil(COUNT_TOTAL/2)
      }
      #self.current_turn = B # R/B
      
      self.id = hashlib.sha256(
        json.dumps(self.board).encode('utf-8')
      ).hexdigest()[:20]

  def clone(self):
    clone = copy.deepcopy(self)
    clone.id = uuid.uuid4().hex # clone must have unique ID
    return clone

  def print(self):
    display = f"\n---- State {self.id} ----\n"
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          val = self.board[layer][row][col]
          display += f"({val})" 
        display += "\n"
      display += "\n" 
    display += f'Blue: {self.count[B]}   Red: {self.count[R]}    '
    display += f'Outcome Class: {self.outcome_class}'
    #display += "Next turn: " + ("Blue" if self.current_turn==B else "Red")
    print(display)

  def play_add(self, color, layer, row, col):
    """Simulate an ADD action.  Return a new State object"""
    if not self.check_availability_to_add(layer, row, col):
      raise Exception("Not available to add.")
    #if self.current_turn != color:
    #  raise Exception(f"Not {color}'s turn.")
    if self.count[color] <= 0:
      raise Exception(f"{color} is out of marbles.")
    new_state = self.clone()
    new_state.board[layer][row][col] = color
    new_state.count[color] -= 1
    #new_state.current_turn = B if color == R else R
    return new_state

  def play_jump(self, color, from_layer, from_row, from_col, to_layer, to_row, to_col):
    if color != self.board[from_layer][from_row][from_col]:
      raise Exception(f"Piece to jump must be {color}.")
    if not self.check_availability_to_jump_here(from_layer, from_row, from_col, to_layer, to_row, to_col):
      raise Exception("Piece to jump is unavailable.")    
    if (to_layer > from_layer):
      raise Exception("Jump must be to a higher level.")
    
    new_state = self.clone()
    new_state.board[to_layer][to_row][to_col] = color
    new_state.board[from_layer][from_row][from_col] = E
    #new_state.current_turn = B if color == R else R   
    return new_state

  def check_availability_to_add(self, layer, row, col):
    if layer < N-1 and layer > -1: 
      if row <= layer and row > -1 and col <= layer and col > -1:
        return (self.board[layer][row][col] == E) and (self.board[layer+1][row][col] != E) and (self.board[layer+1][row+1][col] != E) and (self.board[layer+1][row][col+1] != E) and (self.board[layer+1][row+1][col+1] != E)
      else:
        raise Exception("Row or Column is out of bounds")
    elif layer == N-1: 
      if row <= layer and row > -1 and col <= layer and col > -1:        
        return (self.board[layer][row][col] == E)
      else:
        raise Exception("Row or Column is out of bounds")
    else:
      raise Exception("Layer is out of bounds")
      
  def check_availability_to_jump(self, from_layer, from_row, from_col):
    if from_layer == 0:
      return self.board[from_layer][from_row][from_col] != E    
    elif self.board[from_layer][from_row][from_col] == E:
      return False
    else:
      for above_row, tmp in self.board[from_layer-1].items():
        for above_col, val in tmp.items():
          if (val != E):
            if ((above_row == from_row) or (above_row + 1 == from_row)) and ((above_col == from_col) or (above_col + 1 == from_col)):
              return False
      return True

  def check_availability_to_jump_here(self, from_layer, from_row, from_col, to_layer, to_row, to_col):
    if ((to_row == from_row) or (to_row + 1 == from_row)) and ((to_col == from_col) or (to_col + 1 == from_col)):
      return False
    else:
      return self.check_availability_to_jump(from_layer, from_row, from_col) and self.check_availability_to_add(to_layer, to_row, to_col)

  
  def get_children_add(self, color):
    """Return a list of new child states by adding color"""
    children = []
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          if self.check_availability_to_add(layer, row, col):
            child = self.play_add(color, layer, row, col)
            children.append(child)
    return children
  
  def get_children_jump(self, color):
    """Return a list of new child states by jumping played by a color"""
    children = []
    for from_layer in range(N):
      for from_row in range(from_layer+1):
        for from_col in range(from_layer+1):
          if self.board[from_layer][from_row][from_col] == color:
            for to_layer in range(from_layer):
              for to_row in range(to_layer+1):
                for to_col in range(to_layer+1):
                  if self.check_availability_to_jump_here(from_layer, from_row, from_col, to_layer, to_row, to_col):
                    child = self.play_jump(color, from_layer, from_row, from_col, to_layer, to_row, to_col)
                    children.append(child)
    return children

  def get_all_children(self, color):
    """Return left children"""
    children = self.get_children_jump(color)
    if self.count[color] > 0:
      return children + self.get_children_add(color)
    return children
  
  def compute_outcome_class(self):
    """Return outcome class of this state"""
    if self.id in OC_DICT:
      print('Read existing outcome')
      self.outcome_class = OC_DICT[self.id]
      return self.outcome_class

    outcome = CP # default
    
    sym = self.flip_state()
    if sym.id in OC_DICT:
      print('Flipped board outcome existed')
      sym_outcome = OC_DICT[sym.id]
      if sym_outcome == CR:
        outcome = CL
      if sym_outcome == CL:
        outcome = CR
      if sym_outcome == CN:
        outcome = CN
      OC_DICT[self.id] = outcome
      self.outcome_class = outcome
      return outcome
    
    sym_outcome = CP # default
    if self.board[0][0][0] == E:
      if self.count[B] == 0:
        outcome = CR
        sym_outcome = CL
      elif self.count[R] == 0:
        outcome = CL
        sym_outcome = CR
      else:
        leftOC = self.check_for_CL(B) or self.check_for_CP(B)
        rightOC = self.check_for_CR(R) or self.check_for_CP(R)
        if leftOC and rightOC:
          outcome = CN
          sym_outcome = CN
        if leftOC and not(rightOC):
          outcome = CL
          sym_outcome = CR
        if not(leftOC) and rightOC:
          outcome = CR
          sym_outcome = CL

    self.outcome_class = outcome
    OC_DICT[self.id] = outcome

    sym.outcome_class = sym_outcome
    OC_DICT[sym.id] = sym_outcome
    return outcome
    
  def check_for_CL(self, color):
    """Return whether any children of color are CL"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_outcome_class() == CL:
        return True
    return False

  def check_for_CR(self, color):
    """Return whether any children of color are CR"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_outcome_class() == CR:
        return True
    return False

  def check_for_CP(self, color):
    """Return whether any children of color are CP"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_outcome_class() == CP:
        return True
    return False

  def flip_state(self):
    """Return symmetric board with B/R switched"""
    flip = self.clone()
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          if self.board[layer][row][col] == B:
            flip.board[layer][row][col] = R
          if self.board[layer][row][col] == R:
            flip.board[layer][row][col] = B
    flip.count[B] = self.count[R]
    flip.count[R] = self.count[B]
    return flip
    
def backup_oc_dict():
  open('oc_dict.json', 'w').write(json.dumps(OC_DICT))
  
  
if __name__ == "__main__":
  state = State()
  state.print()
  next_state = state.play_add(R, 2, 0, 0)
  next_state = next_state.play_add(B, 2, 0, 1)
  next_state = next_state.play_add(R, 2, 1, 0)
  next_state = next_state.play_add(B, 2, 1, 1)
  next_state = next_state.play_add(R, 2, 0, 2)
  next_state = next_state.play_add(B, 2, 2, 0)
  next_state = next_state.play_add(R, 2, 2, 2)
  next_state = next_state.play_add(B, 2, 1, 2)
  next_state = next_state.play_add(R, 2, 2, 1)
  next_state.print()
  print("Outcome class for this game is", next_state.compute_outcome_class())
  sym_state = next_state.flip_state()
  sym_state.print()
  print("Outcome class for this game is", sym_state.compute_outcome_class())
  backup_oc_dict()
  
if False:  
  left_children = state.get_all_children(B)
  print("Number of left children:", len(left_children))
  for child in left_children:
    child.print()
    print("Left child outcome class:", child.compute_outcome_class())
  
  right_children = state.get_all_children(R)
  print("Number of right children:", len(right_children))
  for child in right_children:
    child.print()
    print("Right child outcome class:", child.compute_outcome_class())
  


if False: #only works for layer = 3 or higher

#  left_children = next_state.get_all_children(B)
#  print("Number of left children:", len(left_children))
#  for child in left_children:
#    child.print()
#    print("Left child outcome class:", child.outcome_class())

#  right_children = next_state.get_all_children(R)
#  print("Number of right children:", len(right_children))
#  for child in right_children:
#    child.print()
#    print("Right child outcome class:", child.outcome_class())

  if False: #needs the level of 4 or higher
    next_state = state.play_add(B, 3, 0, 0)
    next_state = next_state.play_add(R, 3, 0, 1)
    next_state = next_state.play_add(B, 3, 1, 0)
    next_state = next_state.play_add(R, 3, 1, 1)
    next_state = next_state.play_add(B, 3, 3, 3)
    next_state = next_state.play_add(R, 3, 3, 2)
    next_state.print()
    next_state = next_state.play_jump(2, 0, 0, 3, 3, 3)
    next_state.print()

