import math
import uuid
import copy

N = 4
B, R, E = "B","R", "E" # aliases of colors

class State(object):
  """State of the game"""

  def __init__(self):
    # Unique ID
    self.id = uuid.uuid4().hex
    
    # Represent the game board as a nested dict of tuples
    self.board = {}
    for layer in range(N):
      self.board[layer] = {} 
      for row in range(layer+1):
        self.board[layer][row] = {}
        for col in range(layer+1):
          # Each location contains a tuple (color, availability)
          # - color: R/B/E
          # - availability: True/False
          # At init, only the last layer is available
          self.board[layer][row][col] = [E, layer==N-1]
          
      # Define the player reserves
      count_total = sum([ii*ii for ii in range(1, N+1)])
      self.count = {
        R: math.ceil(count_total/2),
        B: math.ceil(count_total/2)
      }
      self.current_turn = B # R/B

  def clone(self):
    clone = copy.deepcopy(self)
    clone.id = uuid.uuid4().hex # clone must have unique ID
    return clone

  def print(self):
    display = f"\n---- State {self.id} ----\n"
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          val = self.board[layer][row][col][0]
          avail = self.board[layer][row][col][1]
          display += f"({val} {avail}) " 
        display += "\n"
      display += "\n" 
    display += f'Blue: {self.count[B]}   Red: {self.count[R]}    '
    display += "Next turn: " + ("Blue" if self.current_turn==B else "Red")
    print(display)

  def play_add(self, color, layer, row, col):
    """Simulate an ADD action.  Return a new State object"""
    if not self.check_availability_to_add(layer, row, col):
      raise Exception("Not available to add.")
    if self.current_turn != color:
      raise Exception(f"Not {color}'s turn.")
    new_state = self.clone()
    new_state.board[layer][row][col] = [color, True]
    new_state.count[color] -= 1
    new_state.current_turn = B if color == R else R
    new_state.update_availability()
    return new_state

  def play_jump(self, to_layer, to_row, to_col, from_layer, from_row, from_col):
    if self.current_turn != self.board[from_layer][from_row][from_col][0]:
      raise Exception(f"Piece to jump must be {self.current_turn}.")
    if not self.check_availability_to_jump(from_layer, from_row, from_col):
      raise Exception("Piece to jump is blocked.")    
    if (to_layer > from_layer):
      raise Exception("Jump must be to a higher level.")

    color = self.current_turn
    new_state = self.clone()
    new_state.board[to_layer][to_row][to_col] = [color, True]
    new_state.board[from_layer][from_row][from_col] = [E, True]
    new_state.current_turn = B if color == R else R   
    new_state.update_availability()
    return new_state

  def check_availability_to_add(self, layer, row, col):
    if layer < N-1: 
      return (self.board[layer][row][col][0] == E) and (self.board[layer+1][row][col][0] != E) and (self.board[layer+1][row+1][col][0] != E) and (self.board[layer+1][row][col+1][0] != E) and (self.board[layer+1][row+1][col+1][0] != E)
    else: 
      return self.board[layer][row][col][1]

  def check_availability_to_jump(self, layer, row, col):
    if layer == 0:
      return self.board[layer][row][col][0] != E    
    elif self.board[layer][row][col][0] == E:
      return False
    else:
      for above_row, tmp in self.board[layer-1].items():
        for above_col, val in tmp.items():
          if (val[0] != E):
            if ((above_row == row) or (above_row + 1 == row)) and ((above_col == col) or (above_col + 1 == col)):
              return False
      return True
          
    
  def update_availability(self):
    for layer in range(N):
      for row in range(layer+1):
        for col in range(layer+1):
          if self.board[layer][row][col][0] == E:
            self.board[layer][row][col][1] = self.check_availability_to_add(layer, row, col)
          else:
            self.board[layer][row][col][1] = self.check_availability_to_jump(layer, row, col)


if __name__ == "__main__":
  state = State()
  state.print()
  next_state = state.play_add(B, 3, 0, 0)
  next_state = next_state.play_add(R, 3, 0, 1)
  next_state = next_state.play_add(B, 3, 1, 0)
  next_state = next_state.play_add(R, 3, 1, 1)
  next_state = next_state.play_add(B, 3, 3, 3)
  next_state = next_state.play_add(R, 3, 3, 2)
  next_state.print()
  next_state.update_availability()
  next_state.print()
  next_state = next_state.play_jump(2, 0, 0, 3, 3, 3)
  next_state.print()
