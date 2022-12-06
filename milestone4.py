"""
Author: Zachary Jeffreys
Version: 1.0.0
Milestone #2

Hello Grader, thank you for reviewing my assignment. 

How to run this assignment: 
python3 milestone4.py 2048_in.txt 
Enter 0 for Maximizing Current and Minimizing Next Score
Enter 1 for Local Search Algorithm with Minimax

Notes my maximizing current/next works fine, but I ended 
up breaking my local search minimax approach while trying to
add the alpha beta-pruning. I would fix it but I have a 
Distributed Systems Final Exam tomorrow I need to study for. 

As for the extra credit, when it was working, it was able
to change the value of d, and found the max of the 
minimizer, where the minimizer replaces each 0 on the board 
one at a time with a 2 to check for the minimum of the maximizers 
choice. 

Thank you for grading my assignment, 
Zach

"""
import copy
import sys
import os
import random

OUT_FILE = "2048_out.txt"
test_i = 0


class Game():
    """
    Main 2048 Game methods 
    """
    @staticmethod
    def Left(state):
        """
        Move to state left
        @param state: current state
        """
        points = 0
        board = copy.deepcopy(state)
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
        """
        Does required logical calculations
        @param state: current state
        @param row: row to calculate
        """
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
        """
        Converts the board to down state
        @param state: current state of the board
        """
        board = state
        board = Game.transpose(board)
        board, score = Game.Right(board)
        board = Game.transpose(board)
        return (board, score)

    @staticmethod
    def Up(state):
        """
        Up state of board
        @param state: current state of board
        """
        board = state
        board = Game.transpose(board)
        board, score = Game.Left(board)
        board = Game.transpose(board)
        return (board, score)

    @staticmethod
    def Right(state):
        """
        Converts board to Right state
        """
        board = state
        board = Game.reverse(board)
        board, score = Game.Left(board)
        board = Game.reverse(board)
        return (board, score)

    @staticmethod
    def transpose(state):
        """
        Transposes the matrix/board a.e. row to col
        """
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
        """
        Reverses the state of the board
        """
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
        """
        Adds a randomly placed number to the board, 
        default is set to 2, but 4 can also be used
        """
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
        """
        Determines if the state of the game is gameover
        """
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
        """
        Counts all of the zeros at the current state of the board
        """
        board = state
        zeros = 0
        for row_index, row in enumerate(board):
            for col_index, col in enumerate(row):
                if(board[row_index][col_index] == 0):
                    zeros = zeros + 1
        return zeros

    @staticmethod
    def add_two(state):
        """old method for adding too, used add_num instead"""
        board = state
        for i in range(4):
            for j in range(4):
                if(board[i][j] == 0):
                    board[i][j] = 2
                    return board

    def play_game(self, moves):
        """
        Starts an instance of the game
        """
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
    """
    Parses the file
    @param file: file to parse
    """
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
    """
    Write to a specific output_file
    @param games: games to write
    @param output_file: filename to output to
    """
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
    @param board: state of the board
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
    """
    Chooses a random state from a list of states
    @param states: All states possible
    """
    rand_index = random.randint(0, len(states) - 1)
    return states[rand_index]

def choose_best_next_state(states):
    """
    Chooses the best next state based on a list of states
    @param states: All states possible
    """
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
    """
    Chooses the minimum next state based on a list of states
    @param states: All states possible
    """
    min_state = states[0]
    min_state_score = float('inf')
    for state in states:
        s, m = state
        board, score = s
        if(score < min_state_score):
            min_state = state
            min_state_score = score

    # if all states max state is equal to zero choose randomly
    # So it doesn't get stuck in ['L', 'L']
    # if(min_state_score == 0):
    #     min_state = choose_random_state(states)

    return min_state

def run_maximizing_current_minimizing_next_score(board):
    """
    Maximizes the current score and minimizes the next score 
    @param board: current starting state of game
    """
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

def minimax_approach(board, d=2):
    """
    Plays game using Local Search Algorithm with MiniMax Approach
    EC #1) make d modifiable
    EC #2) Use alpha beta pruning
    @param board: start state of board
    @param d: depth first steps 
    """
    end = False
    curr_board = board
    curr_score = 0
   
    while(not end):
        temp_score = 0
        minmax_score, move = minimax_decision(curr_board,d)

        if move == 'L':
            curr_board, temp_score = Game.Left(curr_board)
        elif move == 'U':
            curr_board, temp_score = Game.Up(curr_board)
        elif move == 'R':
            curr_board, temp_score = Game.Right(curr_board)
        elif move == 'D':
            curr_board, temp_score = Game.Down(curr_board)
        curr_score = curr_score + temp_score
                
        curr_board = Game.add_a_random_num(curr_board)

        if(Game.is_game_over(curr_board)):
            print("Final score:", curr_score)
            Game.print_board(curr_board)
            end = True

def minimax_decision(board, d=2):
    """
    Runs minimax algothem with alpha-beta pruning
    @param board: state of board
    @param d: DFS steps to take
    @return (final score, best move maximizer)
    """
    alpha = float('-inf')

    
    v = float('-inf')
    move = "No MinMax best Choose random"
    final_score = 0
    a = alpha
    d = d + 1 #fix indexing issue

    for m in ['L', 'U', 'R', 'D']:
        curr_score = None
        if m == 'L':
            left_state, curr_score = Game.Left(board)
            v = min_value(left_state, 'L', d-1)
    
        elif m =='U': 
            up_state, curr_score = Game.Up(board)
            v = min_value(up_state, 'U', d-1)
            
        elif m == 'R': 
            right_state, curr_score = Game.Right(board)
            v = min_value(right_state, 'R', d-1)
            
        elif m == "D":
            down_state, curr_score = Game.Down(board)
            v = min_value(down_state, 'D', d-1)
            
        if(curr_score > final_score):
            final_score = curr_score
            move = m
            a = v
    print("minmax decision: ", v + final_score, move)
    return a + final_score, move

def max_value(state, move, step, alpha= float('-inf'), beta=float('inf'), score=0):
    """
    returns minimum points possible
    @param state: current state of bame
    @param move: move the occured 
    @param step: steps left until d
    @param alpha: used for alpha beta pruning
    @param beta: used for beta of pruning
    @param score: stored value of max score
    @returns: The max value after minmax algo
    """

    # alpha beta pruning
    if(alpha > beta):
        return score
    if Game.is_game_over(state) or step==0:
        return score

    v = float('-inf')
    alpha = alpha 
    beta = beta 
    for m in ['L', 'U', 'R', 'D']:
        val = None
        if m == 'L':
            left_state, score = Game.Left(state)
            v = min_value(left_state, 'L', step-1, alpha=alpha, beta=beta, score=score)
        elif m =='U': 
            up_state, score = Game.Up(state)
            v = min_value(up_state, 'U', step-1, alpha=alpha, beta=beta, score=score)
        elif m == 'R': 
            right_state, score = Game.Right(state)
            v = min_value(right_state, 'R', step-1, alpha=alpha, beta=beta, score=score)
        elif m == "D":
            down_state, score = Game.Down(state)
            v = min_value(down_state, 'D', step-1, alpha=alpha, beta=beta, score=score)
        if(v > alpha):
            alpha = v
    # print("Returning max value of :", v)
    return max(v, alpha)

def min_value(state, move, step, alpha = float('-inf'), beta=float('inf'), score=0):
    """
    returns minimum points possible
    @param state: current state of bame
    @param move: move the occured 
    @param step: steps left until d
    @param alpha: used for alpha beta pruning
    @param beta: used for beta of pruning
    @param score: stored value of min score

    @return: v the score
    """
    board = state
    #alpha beta pruning
    if(alpha > beta):
        return score
    if Game.is_game_over(state) or step == 0:
        return score

    # Based on what the professor told us in class, I am assuming that 
    # this minimizer should choose the minimum value based on the 
    # location that a 2 is replaced for the 0
    v = float('inf')
    alpha = alpha
    b= beta
    board_with_num = board
    for row_index, row in enumerate(board_with_num):
        for col_index, col in enumerate(row):
            if(board_with_num[row_index][col_index] == 0):
                board_with_num[row_index][col_index] = 2
                v = max_value(board_with_num, '2', step-1, alpha=alpha, beta=b)
                # print(v, b)
                if(v < b):
                    b = v
                board_with_num[row_index][col_index] = 0  
    return b


def setup_game(start_state):
    """
    sets up state of the game by adding two two's
    @param start_state: start state
    @return state after initializing
    """
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
    """
    Handles user input
    @param boards: current state of board
    """
    print("\nWelcome To The 2048 Game!\n")
    playGame = False
    while(not playGame):
        game = int(input("Type 0 to play Maximizing Currant and Minimizing Next, or 1 to play MiniMax Approach: "))
        if(game == 0 or game == 1):
            playGame = True
            if(game == 0):
                print(">>>You Selected Maximizing Currant and Minimizing Next Search\n")
                for start_state in boards:
                    start_state = setup_game(start_state)
                    run_maximizing_current_minimizing_next_score(start_state)
            if(game == 1):
                print(">>>You Selected MiniMax Approach \n")
                d = int(input("Enter value of d: "))
                for start_state in boards:
                    start_state = setup_game(start_state)
                    minimax_approach(start_state, d)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)

    os.system('cls||clear')
    initial_boards, N = parse_file(sys.argv[1])
    start_game(initial_boards)
   

    # Write to output file
    # write_to_file(games, OUT_FILE)

  


