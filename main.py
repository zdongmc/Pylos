import math
import json
import copy


N = 3
COUNT = math.ceil(sum([ii*ii for ii in range(1, N+1)])/2) # total count of red (or blue) marbles 
B, R, E = "B", "R", "E" # aliases of colors
CP, CN, CR, CL =  "CP", "CN", "CR", "CL" # alias of outcome classes


oc_dict = json.load(open('oc_dict.json')) 
print(f"OC DICT size: {len(oc_dict)}")
oc_counter = 0


def save_oc_dict():
  open('oc_dict.json', 'w').write(json.dumps(oc_dict))


class State(object):

  def __init__(self, board=None):
    """Create a new state and board.  If no board is supplied as argument, create an empty board"""

    # Create self.board as a nested dict
    if board is None:
      self.board = {}
      for layer in range(N):
        self.board[layer] = {} 
        for row in range(layer+1):
          self.board[layer][row] = {}
          for col in range(layer+1):
            self.board[layer][row][col] = E 
    else:
      if len(board) != N:
        raise Exception('Failed to create new board')
      self.board = board
     
    # Derive other attributes from self.board
    self.uid = self.encode()


  def encode(self):
    """Encode the board into a string"""
    uid = ""
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          uid += self.board[layer][row][col]
      uid += "-" 
    return uid.rstrip('-')


  def get_count(self, color):
    """Return reserve of a color"""
    count_on_board = self.uid.count(color)
    reserve = COUNT - count_on_board
    return reserve


  def print(self):
    display = f"STATE: {self.uid}\n"
    display += f'Blue: {self.get_count(B)}  Red: {self.get_count(R)}  '
    display += f'OC(disk): {oc_dict.get(self.uid,"??")}'
    display += '\n'
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          val = self.board[layer][row][col]
          display += f"({val})" 
        display += "\n"
    print(display)



  def play_add(self, color, layer, row, col):
    """Simulate an ADD action.  Return new State"""
    if not self.check_availability_to_add(layer, row, col):
      raise Exception("Not available to add.")
    if self.get_count(color) <= 0:
      raise Exception(f"{color} is out of marbles.")

    new_board = copy.deepcopy(self.board)
    new_board[layer][row][col] = color
    return State(new_board)


  def play_jump(self, color, from_layer, from_row, from_col, to_layer, to_row, to_col):
    """Simulate an JUMP action.  Return new State"""
    if color != self.board[from_layer][from_row][from_col]:
      raise Exception(f"Piece to jump must be {color}.")
    if not self.check_availability_to_jump_here(from_layer, from_row, from_col, to_layer, to_row, to_col):
      raise Exception("Piece to jump is unavailable.")    
    if (to_layer > from_layer):
      raise Exception("Jump must be to a higher level.")
    
    new_board = copy.deepcopy(self.board)
    new_board[to_layer][to_row][to_col] = color
    new_board[from_layer][from_row][from_col] = E
    return State(new_board)


  def check_availability_to_add(self, layer, row, col):
    if layer < N-1 and layer > -1: 
      if row <= layer and row > -1 and col <= layer and col > -1:
        out = (
          (self.board[layer][row][col] == E) and 
          (self.board[layer+1][row][col] != E) and 
          (self.board[layer+1][row+1][col] != E) and 
          (self.board[layer+1][row][col+1] != E) and 
          (self.board[layer+1][row+1][col+1] != E)
        )
        return out
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
            if (
              ((above_row == from_row) or (above_row + 1 == from_row)) and 
              ((above_col == from_col) or (above_col + 1 == from_col))
            ):
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
    if self.get_count(color):
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
    """Return all children for a color"""
    jump_children = self.get_children_jump(color)
    add_children = self.get_children_add(color)
    return jump_children + add_children


  def get_equivalence(self):
    """Return 8 equivalent states from rotation/mirro that share the same outcome class"""

    # Rotate 0, 90, 180, 270 and their mirrors
    r0_board = copy.deepcopy(self.board)
    r0m_board = copy.deepcopy(self.board)
    r90_board = copy.deepcopy(self.board)
    r90m_board = copy.deepcopy(self.board)
    r180_board = copy.deepcopy(self.board)
    r180m_board = copy.deepcopy(self.board)
    r270_board = copy.deepcopy(self.board)
    r270m_board = copy.deepcopy(self.board)
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          val = self.board[layer][row][col]
          r0_board[layer][row][col] = val
          r0m_board[layer][col][row] = val
          r90_board[layer][layer-row][col] = val
          r90m_board[layer][col][layer-row] = val
          r180_board[layer][layer-row][layer-col] = val
          r180m_board[layer][layer-col][layer-row] = val
          r270_board[layer][row][layer-col] = val
          r270m_board[layer][layer-col][row] = val
    r0_state = State(r0_board)
    r0m_state = State(r0m_board)
    r90_state = State(r90_board)
    r90m_state = State(r90m_board)
    r180_state = State(r180_board)
    r180m_state = State(r180m_board)
    r270_state = State(r270_board)
    r270m_state = State(r270m_board)

    # Return non-duplicates 
    states = [r0_state, r0m_state, r90_state, r90m_state, r180_state, r180m_state, r270_state, r270m_state] 
    out = {ss.uid: ss for ss in states}
    return list(out.values())


  def compute_oc(self):
    """Compute outcome class of this state"""
    global oc_dict
    global oc_counter

    if self.uid in oc_dict:
      #print(f'Read existing OC: {self.uid}')
      return oc_dict[self.uid]
    else:
      outcome = CP # default

      if self.board[0][0][0] == E:
        if self.get_count(B) == 0:
          outcome = CR
        elif self.get_count(R) == 0:
          outcome = CL
        else:
          left_oc = self.check_for_CL(B) or self.check_for_CP(B)
          right_oc = self.check_for_CR(R) or self.check_for_CP(R)
          if left_oc and right_oc:
            outcome = CN
          if left_oc and not(right_oc):
            outcome = CL
          if not(left_oc) and right_oc:
            outcome = CR

      oc_counter += 1
      print(f'Computed new OC: {self.uid} (total: {oc_counter})')

      # Add equivalent and flip entries to OCT_DICT
      eq_states = self.get_equivalence()
      flip_map = {"CL": "CR", "CR": "CL", "CP": "CP", "CN": "CN"}
      for eq_state in eq_states:
          oc_dict[eq_state.uid] = outcome # save equivalent cases
          flip_eq_state = eq_state.flip()
          oc_dict[flip_eq_state.uid] = flip_map[outcome] # save flip cases

      return outcome
  

  def check_for_CL(self, color):
    """Return whether any children of color are CL"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_oc() == CL:
        return True
    return False


  def check_for_CR(self, color):
    """Return whether any children of color are CR"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_oc() == CR:
        return True
    return False


  def check_for_CP(self, color):
    """Return whether any children of color are CP"""
    children = self.get_all_children(color)
    for child in children:
      if child.compute_oc() == CP:
        return True
    return False


  def flip(self):
    """Return new state with symmetric board with B/R switched"""
    flip_board = copy.deepcopy(self.board)
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          if flip_board[layer][row][col] == B:
            flip_board[layer][row][col] = R
          elif flip_board[layer][row][col] == R:
            flip_board[layer][row][col] = B
    return State(flip_board)


  
def test():
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
  print("Outcome class for this game is", next_state.compute_oc())
  sym_state = next_state.flip_state()
  sym_state.print()
  print("Outcome class for this game is", sym_state.compute_oc())
  backup_oc_dict()
 
  if False:
    left_children = state.get_all_children(B)
    print("Number of left children:", len(left_children))
    for child in left_children:
      child.print()
      print("Left child outcome class:", child.compute_oc())
    
    right_children = state.get_all_children(R)
    print("Number of right children:", len(right_children))
    for child in right_children:
      child.print()
      print("Right child outcome class:", child.compute_oc())

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


def test_children():
  state = State()
  state.print()
  child_states = state.get_all_children(B)
  for ii, child_state in enumerate(child_states):
    gchild_states = child_state.get_all_children(R)
    for jj, gchild_state in enumerate(child_states):
      print(f"{ii}, {jj}")
      gchild_state.print()


def test_n3():
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
  next_state = next_state.play_jump(R, 2, 2, 2, 1, 0, 0)
  next_state.print()
  next_state = next_state.flip()
  next_state.print()


def test_compute_oc():
  state = State()
  state.compute_oc()
  state.print()
  print(f'OC Counter: {oc_counter}')
  save_oc_dict()


def test_n3_1():
  state = State()
  state = print()


def test_equivalence():
  state = State()
  next_state = state.play_add(R, 2, 0, 0)
  next_state = next_state.play_add(B, 2, 0, 1)
  next_state = next_state.play_add(R, 2, 1, 0)
  next_state = next_state.play_add(B, 2, 1, 1)
  next_state = next_state.play_add(R, 2, 0, 2)
  next_state = next_state.play_add(B, 2, 2, 0)
  next_state = next_state.play_add(R, 2, 2, 2)
  next_state = next_state.play_add(B, 2, 1, 2)
  next_state = next_state.play_add(B, 1, 0, 0)
  for eq_state in next_state.get_equivalence():
     eq_state.print() 


def test_jojo():
  state = State()
  child_states = state.get_all_children()
  for child_state in child_states:
      child_state.print()

def get_oc(uid):
  print(f"{uid} is {oc_dict[uid]}")

if __name__ == "__main__":
    test_compute_oc()
    #test_jojo()
    #get_oc('E-EEEE-EEEEEEEEE')
    #get_oc('E-EEEE-REEEEEEEE')
    #get_oc('E-EEEE-EREEEEEEE')
    #get_oc('E-EEEE-EEEEREEEE')
