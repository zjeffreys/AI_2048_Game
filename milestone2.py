"""
Author: Zachary Jeffreys
Version: 1.0.0
Milestone #2
"""
import sys
import os
import random

OUT_FILE = "2048_out.txt"

class Game():
    
    @staticmethod
    def Left(state):
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
    def add_a_random_num(state, number = 2, include_second_num = False):
        num = number

        #choose two or four at random
        if(include_second_num):
            num = random.randrange(2, 5, 2)

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
                        board[row_index][col_index] = num
                        return board
        return board #shouldn't ever reach here 

    @staticmethod
    def is_game_over(state):
        isOver = False
        isAllZero = True

        if(Game.count_zeros(state) == 0):
            scores = []
            states = generate_all_next_states(state)
            for board in states:
                s, m = board
                board, score = s
                scores.append(score)
            for s in scores:
                if s > 0:
                    isAllZero = False
            if(isAllZero):
                isOver = True
                print("No More Moves")

               

        
        return isOver

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
            max_state_score = score

    # if all states max state is equal to zero choose randomly
    # So it doesn't get stuck in ['L', 'L']
    if(max_state_score == 0):
        max_state = choose_random_state(states)

    return max_state

def run_random_local_search(board, N=100):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []

    print("Randomly select one of the next states that has an Non-zero Current Score + Next Score:")
    for i in range(N): 
        gen_next_states = generate_all_next_states(current_state[0])
        next_state, next_move = choose_random_state(gen_next_states)   

        # Add a Random 2 or 4 to board
        current_state = (Game.add_a_random_num(next_state[0]), next_state[1], True)
        moves.append(next_move)
        text = "Current Score({curr}) + Next Score({next}) = {final}".format(curr=curr_score, next=current_state[1], final=curr_score + current_state[1])
        print(text)
        curr_score =curr_score + current_state[1]

        current_state = current_state # some local var error 

        #if there are no more moves Game Over
        if(Game.is_game_over(current_state[0])):
            print("Game Over")
            break

        if(curr_score == 0): 
            print("current score + next score is zero...GAME OVER")
            break
        if(curr_score == 2048):
            print("WINNER WINNER CHICKEN DINNER!! GREAT JOB!")
            exit(1)
            break

        trials = trials + 1
    proper_data_structure = {
        "final_score": curr_score, 
        "sequence_of_moves": moves, 
        "final_arrangment": current_state[0]
    }
    print("\nFinal Board:")
    Game.print_board(current_state[0])
    print("Score:", proper_data_structure["final_score"], ". Trials:", trials, " Moves:", proper_data_structure["sequence_of_moves"])
    print()

def run_maximizing_local_search(board, N=25):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []

    print("Randomly select one of the next states that has the maximum current and next score: ")
    for i in range(N): 
        gen_next_states = generate_all_next_states(current_state[0])
        next_state, next_move = choose_best_next_state(gen_next_states)   

        # Add a random 2 or 4 to board
        current_state = (Game.add_a_random_num(next_state[0]), next_state[1], True) 
        moves.append(next_move)
        text = "Current Score({curr}) + Next Score({next}) = {final}".format(curr=curr_score, next=current_state[1], final=curr_score + current_state[1])
        print(text)
        curr_score =curr_score + current_state[1]

        if(Game.is_game_over(current_state[0])):
            print("Game Over")
            break

        if(curr_score == 0): 
            print("current score + next score is zero...Game Over.")
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
    print("\nFinal Board:")
    Game.print_board(current_state[0])
    print("Score:", proper_data_structure["final_score"], ". Trials:", trials, " Moves:", proper_data_structure["sequence_of_moves"])
    print()

def setup_game(start_state):
    board = start_state
    print("Initial 2048 Board")
    Game.print_board(board)

    # Add two 2's randomly placed on board
    print("Board afer adding 2 randomly places twos: ")
    one = Game.add_a_random_num(board)
    two = Game.add_a_random_num(one)
    Game.print_board(two)
    return two

def start_game(boards):
    print("\nWelcome To The 2048 Game!\n")
    playGame = False
    while(not playGame):
        game = int(input("Type 0 to play Random_Local_Seach, or 1 to play Max_Local_Search: "))
        if(game == 0 or game == 1):
            playGame = True
            if(game == 0):
                print(">>>You Selected Random Local Search\n")
                N = int(input("How many iterations should I run? (Press Enter for 100): ") or 100) 
                for start_state in boards:
                    start_state = setup_game(start_state)
                    run_random_local_search(start_state, N=N)
            if(game == 1):
                print(">>>You Selected Maximizing Local Search\n")
                N = int(input("How many iterations should I run? (Press Enter for 25): ")or 25) 
                for start_state in boards:
                    start_state = setup_game(start_state)
                    run_maximizing_local_search(start_state, N)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)

    os.system('cls||clear')
    initial_boards, N = parse_file(sys.argv[1])
    start_game(initial_boards)

    # write_to_file(games, OUT_FILE)

  


