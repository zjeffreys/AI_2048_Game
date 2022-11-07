"""
Author: Zachary Jeffreys
Version: 1.0.0
Milestone #2
"""
import sys
import random

OUT_FILE = "2048_out.txt"

class Game():
  
    def __init__(self, init_board):
        self.board = init_board
    
    def Left(self):
        points = 0
        for index, row in enumerate(self.board):
            for i in range(len(row) - 1):
                if(row[i] == row[i + 1] and row[i] != 0):
                    points = row[i] * 2
                    row[i] = row[i] + row[i + 1]
                    row[i + 1] = 0
                self.bubble(index)
        return(points)

    def bubble(self, row):
        col = 3
        while(col != 0):
            if((self.board[row][col] != 0) and (self.board[row][col - 1] == 0)):
                self.board[row][col-1] = self.board[row][col]
                self.board[row][col] = 0
            col = col - 1

    def Down(self):
        self.transpose()
        score = self.Right()
        self.transpose()
        return score

    def Up(self):
        self.transpose()
        score = self.Left()
        self.transpose()
        return score

    def Right(self):
        self.reverse()
        score = self.Left()
        self.reverse()
        return score

    def transpose(self):
        new_board = []
        for i in range(4):
            new_board.append([])
            for j in range(4):
                new_board[i].append(self.board[j][i])
        self.board = new_board
   
    def reverse(self):
        new_board =[]
        for i in range(4):
            new_board.append([])
            for j in range(4):
                new_board[i].append(self.board[i][3 - j])
        self.board = new_board
    
    def add_a_random_num(self, number = 2):
        zero_index = random.randint(1, self.count_zeros())
        index = 0
        print("Random: ", zero_index)
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if(self.board[row_index][col_index] == 0):
                    index = index + 1
                    if(index == zero_index):
                        self.board[row_index][col_index] = number
                    

    def count_zeros(self):
        zeros = 0
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if(self.board[row_index][col_index] == 0):
                    zeros = zeros + 1
        return zeros

    def add_two(self):
        for i in range(4):
            for j in range(4):
                if(self.board[i][j] == 0):
                    self.board[i][j] = 2
                    return

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

    def print_board(self):
        for i in range(4):
            print(self.board[i])
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

def run_random_search(boards):
    board = boards[0]
    game = Game(board)
    game.print_board()
    game.add_a_random_num()
    game.print_board()
 


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)
    initial_boards, N = parse_file(sys.argv[1])
    run_random_search(initial_boards)
   
    
    # games = run_random_search(boards)

    # write_to_file(games, OUT_FILE)

  


