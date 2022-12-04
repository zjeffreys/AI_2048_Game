"""
Author: Zachary Jeffreys
Version: 1.0.0
Milestone #2
"""
import copy
import sys
import os
import random

OUT_FILE = "2048_out.txt"
test_i = 0


class Game():
    
    @staticmethod
    def Left(state):
        points = 0
        board = state
        for i, row in enumerate(board):
            for j in range(len(row) - 1):
                if(row[j] == row[j + 1] and row[j] != 0):
                    points = points + row[j] * 2
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
        num = number
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
    2(ED, EU, ER, EL) 
    """

    # ASSUMPTION: I am assuming that we move left than add a 2 or 4
    board_after_adding_random_2 = Game.add_a_random_num(board)
    board_after_adding_random_4 = Game.add_a_random_num(board, number=4)

    # Add random 2 then move (L, U, R, D)
    state_left_2 = (Game.Left(board_after_adding_random_2), 'L')
    state_up_2 = (Game.Up(board_after_adding_random_2), 'U')
    state_right_2 = (Game.Right(board_after_adding_random_2), 'R')
    state_down_2 = (Game.Down(board_after_adding_random_2), 'D')

    # Add random 4 then move (L, U, R, D)
    state_left_4 = (Game.Left(board_after_adding_random_4), 'L')
    state_up_4 = (Game.Up(board_after_adding_random_4), 'U')
    state_right_4 = (Game.Right(board_after_adding_random_4), 'R')
    state_down_4 = (Game.Down(board_after_adding_random_4), 'D')

    states = [state_left_2, state_up_2, state_right_2, state_down_2, state_left_4, state_up_4, state_right_4, state_down_4]
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

def choose_next_minimum_state(states):
    min_state = states[0]
    min_state_score = 0
    for state in states:
        s, m = state
        board, score = s
        if(score < min_state_score):
            min_state = state
            min_state_score = score

    # if all states max state is equal to zero choose randomly
    # So it doesn't get stuck in ['L', 'L']
    if(min_state_score == 0):
        min_state = choose_random_state(states)

    return min_state
# milestone 4 algorithms 
def run_maximizing_current_minimizing_next_score(board, N=100):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []
    end = False
    isMaxTurn = True
    maxTurns = 0
    minTurns = 0
    next_state = None
    next_move = None

    print("maximizing current minimizing next score until no more available moves:")
    while (not end):
        trials = trials + 1
        gen_next_states = generate_all_next_states(current_state[0])
        if(isMaxTurn):
            print("Max's turn")
            maxTurns = maxTurns + 1
            next_state, next_move = choose_best_next_state(gen_next_states)   
            isMaxTurn = False
        else:
            print("Min's Turn")
            minTurns = minTurns + 1
            next_state, next_move = choose_next_minimum_state(gen_next_states)   
            isMaxTurn = True


        current_state = (next_state[0], next_state[1], True)
        moves.append(next_move)
        text = "Current Score({curr}) + Next Score({next}) = {final}".format(curr=curr_score, next=current_state[1], final=curr_score + current_state[1])
        print(text)
        curr_score =curr_score + current_state[1]

        current_state = current_state # some local var error 

        #if there are no more moves Game Over
       
        if(Game.is_game_over(current_state[0])):
            print("Game Over")
            end = True
            break

        # I don't understand when the curr and next score will ever be 0 but in the very beginning 
        # or in an infinite loop so added inf loop
        not_on_first_few_moves = 0
        MAX_BEFORE_ERROR = 20
        if(curr_score == 0 and not_on_first_few_moves > MAX_BEFORE_ERROR): 
            print("current score + next score is zero...GAME OVER")
            break

        if(curr_score == 2048):
            print("WINNER WINNER CHICKEN DINNER!! GREAT JOB!")
            break

        
    proper_data_structure = {
        "final_score": curr_score, 
        "sequence_of_moves": moves, 
        "final_arrangment": current_state[0]
    }
    print("\nFinal Board:")
    Game.print_board(current_state[0])
    print("Score:", proper_data_structure["final_score"], ". Trials:", trials, " Moves:", proper_data_structure["sequence_of_moves"])
    print()

def minimax_decision(board, N=100, d=3):
    v = float('-inf')
    m = None
    score = 0
    print("minmax_decesion (choose max of these):")

    for m in ['L', 'U', 'R', 'D']:
        val = None
        curr_score = None
        if m == 'L':
            val = min_value(Game.Left(board), 'L', d-1)
            curr_score = Game.Left(board)[1]
        elif m =='U': 
            val = min_value(Game.Up(board), 'U', d-1)
            curr_score = Game.Up(board)[1]
            
        elif m == 'R': 
            val = min_value(Game.Right(board), 'R', d-1)
            curr_score = Game.Right(board)[1]
            
        elif m == "D":
            val = min_value(Game.Down(board), 'D', d-1)
            curr_score = Game.Down(board)[1]
            
            
        if(curr_score > score):
            score = curr_score
            v = val[0]
            m = val[1]
    print(v, score, m)
    return v + score, m

def max_value(state, move, step):
    """:returns minimum points possible"""
    board = state[0]
    # print("maximizer returns: ", state[1], move)
    if Game.is_game_over(state[0]) or step==0:
        # print("max_value() returns:", state[1], move)

        return state[1], move

    v = float('-inf')
    for m in ['L', 'U', 'R', 'D']:
        val = None
        if m == 'L':
            b = copy.deepcopy(board)
            val = min_value(Game.Left(b), 'L', step-1)
        elif m =='U': 
            b = copy.deepcopy(board)
            val = min_value(Game.Up(b), 'U', step-1)
        elif m == 'R': 
            b = copy.deepcopy(board)
            val = min_value(Game.Right(b), 'R', step-1)
        elif m == "D":
            b = copy.deepcopy(board)
            val = min_value(Game.Down(b), 'D', step-1)

        if(val[0] > v):
            v = val[0]
    # print("Returning max value of :", v)
    return v, move

def min_value(state, move, step):
    """ Goal: find best place to add a 2 or 4 to minimize the maximum next move"""
    board = state[0]
    if Game.is_game_over(state[0]) or step == 0:
        # print("Break case min:", state[1])
        return state[1], move

    v = float('inf')
    board_with_num = board
    for row_index, row in enumerate(board_with_num):
        for col_index, col in enumerate(row):
            if(board_with_num[row_index][col_index] == 0):
                board_with_num[row_index][col_index] = 2
                # edit from algorithem since i want to min of the max placement for zero 
                max = float("-inf")
                for m in ['L', 'U', 'R', 'D']:
                    val = None
                    if m == 'L':
                        b = copy.deepcopy(board_with_num)
                        val = max_value(Game.Left(b), 'L', step-1)
                    elif m =='U': 
                        b = copy.deepcopy(board_with_num)
                        val = max_value(Game.Up(b), 'U', step-1)
                    elif m == 'R': 
                        b = copy.deepcopy(board_with_num)
                        val = max_value(Game.Right(b), 'R', step-1)
                    elif m == "D":
                        b = copy.deepcopy(board_with_num)
                        val = max_value(Game.Down(b), 'D', step-1)

                    if(val[0] > max):
                       max = val[0]
                # return minimum of max zero placement
                if(max < v):
                    v = max   
                board_with_num[row_index][col_index] = 0  
                print("returning min value of: ", v)
    return v, move

def local_search_algorithm_with_minmax_approach(board, N, steps = 2):
    curr_score = 0
    current_state = (board, 0)
    trials = 0
    moves = []
    end = False
    next_state = None
    next_move = None

    print("Running minmax: ")
    while (not end):
        trials = trials + 1
        next_state, next_move = minimax_decision(board)   # returns move based on min max algorithm 

            

        # if(isMaxTurn):
        #     print("Max's turn")
        #     maxTurns = maxTurns + 1
        #     next_state, next_move = choose_best_next_state(gen_next_states)   
        #     isMaxTurn = False
        # else:
        #     print("Min's Turn")
        #     minTurns = minTurns + 1
        #     next_state, next_move = choose_next_minimum_state(gen_next_states)   
        #     isMaxTurn = True


        current_state = (next_state[0], next_state[1], True)
        moves.append(next_move)
        text = "Current Score({curr}) + Next Score({next}) = {final}".format(curr=curr_score, next=current_state[1], final=curr_score + current_state[1])
        print(text)
        curr_score =curr_score + current_state[1]

        current_state = current_state # some local var error 

        #if there are no more moves Game Over
       
        if(Game.is_game_over(current_state[0])):
            print("Game Over")
            end = True
            break

        # I don't understand when the curr and next score will ever be 0 but in the very beginning 
        # or in an infinite loop so added inf loop
        not_on_first_few_moves = 0
        MAX_BEFORE_ERROR = 20
        if(curr_score == 0 and not_on_first_few_moves > MAX_BEFORE_ERROR): 
            print("current score + next score is zero...GAME OVER")
            break

        if(curr_score == 2048):
            print("WINNER WINNER CHICKEN DINNER!! GREAT JOB!")
            break

        
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
        game = int(input("Type 0 to play Maximizing Currant and Minimizing Next, or 1 to play Local Search Algorithm with MiniMax Approach: "))
        if(game == 0 or game == 1):
            playGame = True
            if(game == 0):
                print(">>>You Selected Random Local Search\n")
                N = int(input("How many iterations should I run? (Press Enter for 100): ") or 100) 
                for start_state in boards:
                    start_state = setup_game(start_state)
                    run_maximizing_current_minimizing_next_score(start_state, N=N)
            if(game == 1):
                print(">>>You Selected Maximizing Local Search\n")
                N = int(input("How many iterations should I run? (Press Enter for 25): ")or 25) 
                for start_state in boards:
                    start_state = setup_game(start_state)
                    local_search_algorithm_with_minmax_approach(start_state, N)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)

    os.system('cls||clear')
    initial_boards, N = parse_file(sys.argv[1])
    #start_game(initial_boards)
    print("Original")

    Game.print_board(initial_boards[0])
    print(minimax_decision(initial_boards[0]))

    # Write to output file
    # write_to_file(games, OUT_FILE)

  


