"""
Author: Zachary Jeffreys
Version: 1.0.0
Milestone #2
"""
import sys
import random

OUT_FILE = "2048_out.txt"

class Game():
  
    # def __init__(self, init_board):
    #     print('nil')
    #     self.board = init_board
    
    @staticmethod
    def Left(state):
        
        """
        This method creates takes in a state, and returns 
        a new state after moving the game pieces left

        @param state: A 2D array describing the start state of the board
        @return A tuple consisting of the new 2D array and points score from move
        """
        points = 0
        board = state
        for i, row in enumerate(board):
            for j in range(len(row) - 1):
                if(row[j] == row[j + 1] and row[j] != 0):
                    points = row[j] * 2
                    row[j] = row[j] + row[j + 1]
                    row[j + 1] = 0
                board = Game.bubble(board, i)
        return (board, points) 

    @staticmethod
    def bubble(state, row):
        board = state
        col = 3
        while(col != 0):
            if((board[row][col] != 0) and (board[row][col - 1] == 0)):
                board[row][col-1] = board[row][col]
                board[row][col] = 0
            col = col - 1
        return board

    @staticmethod
    def Down(state):
        board = state
        board = Game.transpose(board)
        board, score = Game.Right(board)
        board = Game.transpose(board)
        return (board, score)

    @staticmethod
    def Up(state):
        board = state
        board = Game.transpose(board)
        board, score = Game.Left(board)
        board = Game.transpose(board)
        return (board, score)

    @staticmethod
    def Right(state):
        board = state
        board = Game.reverse(board)
        board, score = Game.Left(board)
        board = Game.reverse(board)
        return (board, score)

    @staticmethod
    def transpose(state):
        new_board = []
        board = state
        for i in range(4):
            new_board.append([])
            for j in range(4):
                new_board[i].append(board[j][i])
        board = new_board
        return board
   
    @staticmethod
    def reverse(state):
        board = state
        new_board =[]
        for i in range(4):
            new_board.append([])
            for j in range(4):
                new_board[i].append(board[i][3 - j])
        board = new_board
        return board
    
    @staticmethod
    def add_a_random_num(state, number = 2):
        board = state
        zero_index = Game.count_zeros(board)
        if(zero_index == 0): # no more zeros just return original board
            return state
        zero_index = random.randint(1, zero_index)
        index = 0
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if(board[row_index][col_index] == 0):
                    index = index + 1
                    if(index == zero_index):
                        board[row_index][col_index] = number
                        return board
        return board #shouldn't ever reach here 
                    

    @staticmethod
    def count_zeros(state):
        board = state
        zeros = 0
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if(board[row_index][col_index] == 0):
                    zeros = zeros + 1
        return zeros

    @staticmethod
    def add_two(state):
        board = state
        for i in range(4):
            for j in range(4):
                if(board[i][j] == 0):
                    board[i][j] = 2
                    return board

    def play_game(self, moves):
        score = 0
        for move in moves:
            if(move == "L"):
                score = score + self.Left()
            elif(move =="R"):
                score = score + self.Right()
            elif(move =="U"):
                score = score + self.Up()
            elif(move == "D"):
                score = score + self.Down()
        self.add_two()
        return score

    @staticmethod
    def print_board(state):
        board = state
        for i in range(4):
            print(board[i])
        print("")
  
def parse_file(file):
        boards = []
        N = 0
        with open(file) as f:
            r = 0
            board = []
            file_line = 0
            for index, line in enumerate(f.readlines()):
                if(index == 0):
                    n = line.split()
                    N = int(n[0])
                else:
                    board.append([int(x) for x in line.split(',')])
                    if(file_line == 3):
                        boards.append(board)
                        board = []
                        file_line = 0
                    else:
                        file_line = file_line + 1
        return (boards, N)

def write_to_file(games, output_file):
    formatted_score = ""
    for g in games:
        score = str(g[1])
        for move in g[0]:
            score = score + "," + move
        formatted_score = formatted_score + score + "\n"

    f = open(output_file, "w")
    f.write(formatted_score)
    f.close()

def generate_all_next_states(board):
    """
    Generates all states and returns them as a list
    """

    state_left = (Game.Left(board), 'L')
    state_up = (Game.Up(board), 'U')
    state_right = (Game.Right(board), 'R')
    state_down = (Game.Down(board), 'D')
    states = [state_left, state_up, state_right, state_down]

    return states

def choose_random_state(states):
    rand_index = random.randint(0, len(states) - 1)
    return states[rand_index]

def choose_best_next_state(states):
    max_state = states[0]
    max_state_score = 0
    for state in states:
        s, m = state
        board, score = s
        if(score > max_state_score):
            max_state = state
    return max_state


def run_random_local_search(board, N=100):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []

    print("Initial 2048 Board")
    Game.print_board(board)

    for i in range(N): 
        gen_next_states = generate_all_next_states(current_state[0])
        next_state, next_move = choose_random_state(gen_next_states)   
        current_state = (Game.add_a_random_num(next_state[0]), next_state[1])
        Game.print_board(next_state[0])
        moves.append(next_move)
        curr_score =curr_score + current_state[1]
        if(curr_score == 0): 
            print("current score + next score is zero")
            break
        if(curr_score == 2048):
            print("WINNER WINNER CHICKEN DINNER!! GREAT JOB!")
            break

        trials = trials + 1
    proper_data_structure = {
        "final_score": curr_score, 
        "sequence_of_moves": moves, 
        "final_arrangment": current_state[0]
    }
    print("Final Board:")
    Game.print_board(current_state[0])
    print("Score:", proper_data_structure["final_score"], ". Trials:", trials, " Moves:", proper_data_structure["sequence_of_moves"])
    print()

def run_maximizing_local_search(board, N=25):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []

    print("Initial 2048 Board")
    Game.print_board(board)

    for i in range(N): 
        gen_next_states = generate_all_next_states(current_state[0])
        next_state, next_move = choose_best_next_state(gen_next_states)   
        current_state = (Game.add_a_random_num(next_state[0]), next_state[1])
        Game.print_board(next_state[0])
        moves.append(next_move)
        curr_score =curr_score + current_state[1]
        if(curr_score == 0): 
            print("current score + next score is zero")
            break
        if(curr_score == 2048):
            print("WINNER WINNER CHICKEN DINNER!! GREAT JOB!")
            break

        trials = trials + 1
    proper_data_structure = {
        "final_score": curr_score, 
        "sequence_of_moves": moves, 
        "final_arrangment": current_state[0]
    }
    print("Final Board:")
    Game.print_board(current_state[0])
    print("Score:", proper_data_structure["final_score"], ". Trials:", trials, " Moves:", proper_data_structure["sequence_of_moves"])
    print()



   
 


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)
    initial_boards, N = parse_file(sys.argv[1])
    run_random_local_search(initial_boards[0])

    run_maximizing_local_search(initial_boards[0])

   
    

    # write_to_file(games, OUT_FILE)

  


