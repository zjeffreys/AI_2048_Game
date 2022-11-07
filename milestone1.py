"""
Author: Zachary Jeffreys
Version: 1.0.0

2048 Game Breadth First Search Algorithm


Attribution: I reviewed https://www.geeksforgeeks.org/2048-game-in-python/ to understand 2048 game, used my own code though. 
"""
import sys

GAME_FILE = sys.argv[1]
OUT_FILE = "2048_out.txt"

class Game():
    # INPUT: In
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

class BFS():
    def __init__(self, board):
        self.queue = []
        initial_nodes = [ ("L", 0), ("R", 0), ("U", 0), ("D", 0) ]
        for node in initial_nodes:
            self.queue.append(node)
        self.visited = []
        self.run(board)
        
    
    def max_score(self):
        score = ("___", -1)
        for node  in self.visited:
            if node[1] > score[1]:
                score = node
        return score

    def run(self, board):
        while(len(self.queue) > 0):
            node = self.queue.pop(0)
            if(node not in self.visited):
                game = Game(board)        
                score = game.play_game(node[0])
                node = (node[0], score)
                self.visited.append(node)
                self.update_queue(node[0])
               # print("Final Scores (",node[0],"): ", score)
    
    def update_queue(self, moves):
        if(len(moves) < 3):
            left = moves + 'L'
            right = moves + 'R'
            up = moves + 'U'
            down = moves + 'D'
            #print("update queue(left): ", left)
            self.queue.append((left, 0))
            self.queue.append((right, 0))
            self.queue.append((up, 0))
            self.queue.append((down, 0))
    



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 play.py 2048_in.txt")
        exit(1)

    # Parse File
    N = 0
    boards = []
    with open(GAME_FILE) as f:
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

    # Play game N amount of time
    games = []
    for b in boards:
        bfs = BFS(b)
        games.append(bfs.max_score())


    # Output score to file
    formatted_score = ""
    for g in games:
        score = str(g[1])
        for move in g[0]:
            score = score + "," + move
        formatted_score = formatted_score + score + "\n"

    f = open(OUT_FILE, "w")
    f.write(formatted_score)
    f.close()