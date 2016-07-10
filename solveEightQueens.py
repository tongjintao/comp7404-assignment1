import random
import copy
from optparse import OptionParser

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        solutionCounter = 0
        lectureCase = [[]]
        if lectureExample:
            lectureCase = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", "q", ".", ".", ".", "."],
            ["q", ".", ".", ".", "q", ".", ".", "."],
            [".", "q", ".", ".", ".", "q", ".", "q"],
            [".", ".", "q", ".", ".", ".", "q", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ]
        for i in range(0,numberOfRuns):
            if self.search(Board(lectureCase), verbose).getNumberOfAttacks() == 0:
                solutionCounter+=1
        print "Solved:",solutionCounter,"/",numberOfRuns

    def search(self, board, verbose):
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print "iteration ",i
                print newBoard.toString()
                print newBoard.getCostBoard().toString()
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks) = newBoard.getBetterBoard()
            i+=1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [["." for i in range(0,8)] for j in range(0,8)]
        for i in range(0,8):
            tmpSquareArray[random.randint(0,7)][i] = "q"
        return tmpSquareArray
          
    def toString(self):
        s = ""
        for i in range(0,8):
            for j in range(0,8):
                s += str(self.squareArray[i][j]) + " "
            s += "\n"
        return s + "# attacks: "+str(self.getNumberOfAttacks())

    def getCostBoard(self):
        costBoard = copy.deepcopy(self)
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard


    def getBetterBoard(self):
        #TODO: put your code here...

        betterBoard = copy.deepcopy(self)
        minNumberOfAttacks = self.getNumberOfAttacks() 
        costBoard = self.getCostBoard()
        minCost = 0

        for r in range(0,8):
            for c in range(0,8):
                if costBoard.squareArray[r][c] != "q":
                    minCost += costBoard.squareArray[r][c]

        #steepest hill climbing
        for r in range(0,8):
            for c in range(0,8):
                if self.squareArray[r][c] == "q":
                    for rr in range(0,8):
                        if rr!=r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = "."
                            testboard.squareArray[rr][c] = "q"

                            #pick the step that minimie the total number of attacks in the board
                            if testboard.getNumberOfAttacks() < minNumberOfAttacks:
                                betterBoard = copy.deepcopy(testboard)
                                minNumberOfAttacks = testboard.getNumberOfAttacks()
        
        return (betterBoard, minNumberOfAttacks)

    def getNumberOfAttacks(self):
        #TODO: put your code here...
        number = 0

        # for horitzontal  
        for i in range(0,8):
            countHorizontal = 0
            for j in range(0,8):
                if self.squareArray[i][j] == 'q':
                    countHorizontal += 1
            number += countHorizontal * (countHorizontal - 1) / 2

        # for vertical
        for i in range(0,8):
            countVertical = 0
            for j in range(0,8):
                if self.squareArray[j][i] == 'q':
                    countVertical += 1
            number += countVertical * (countVertical - 1) / 2

        # for diagonal from the right
        for c in range(0,16):
            countDiagonal = 0
            for i in range(0,c+1):
                if c-i < 8 and i<8:
                    if self.squareArray[i][c-i] == 'q':
                        countDiagonal += 1
            number += countDiagonal * (countDiagonal - 1) / 2

        # for diagonal from the right
        for c in range(0,16):
            countDiagonal = 0
            for i in range(0,c+1):
                if 7-c+i >= 0 and i<8:
                    if self.squareArray[i][7-c+i] == 'q':
                        countDiagonal += 1
            number += countDiagonal * (countDiagonal - 1) / 2
    
        
        return number

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    #random.seed(0)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)