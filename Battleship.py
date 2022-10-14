import random, sys

BOARD_COLOMN_LABELS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
BOARD_ROW_LABELS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

EMPTY_SPACE = ' '

NUM_OF_SHIPS_ON_BOARD = {'admiral' : 1 }# , 'cruiser' : 2, 'destroyer' : 3, 'submarine' : 4}
SHIP_LENGTHS = {'admiral' : 5, 'cruiser' : 4, 'destroyer' : 3, 'submarine' : 2}

BOARD_TEMPLATE = """
      A B C D E F G H I J
     ---------------------
  1 | {} {} {} {} {} {} {} {} {} {} |
  2 | {} {} {} {} {} {} {} {} {} {} |
  3 | {} {} {} {} {} {} {} {} {} {} |
  4 | {} {} {} {} {} {} {} {} {} {} |
  5 | {} {} {} {} {} {} {} {} {} {} |
  6 | {} {} {} {} {} {} {} {} {} {} |
  7 | {} {} {} {} {} {} {} {} {} {} |
  8 | {} {} {} {} {} {} {} {} {} {} |
  9 | {} {} {} {} {} {} {} {} {} {} |
 10 | {} {} {} {} {} {} {} {} {} {} |
     ---------------------
"""

def main():

	boardWithShips, boardWithoutShips, deployedShips = boardSetup()
	
	while True:
	
		displayBoard(boardWithoutShips)
		print()
		print()
		displayBoard(boardWithShips)
	
		playerTarget = getPlayerMove(boardWithoutShips)
		makePlayerMove(boardWithoutShips,playerTarget, deployedShips)

def boardSetup():
	
	deployedShips = {}
	
	boardWithoutShips = {}
	for row in range(10):
	    for colomn in range(10):
	        boardWithoutShips[(colomn, row)] = EMPTY_SPACE
	        
	boardWithShips = {}
	for row in range(10):
	    for colomn in range(10):
	        boardWithShips[(colomn, row)] = EMPTY_SPACE
	        
	boardWithShips = getNewBoard(boardWithShips, deployedShips)
	
	return boardWithShips, boardWithoutShips, deployedShips

def getNewBoard(board, ships_on_board):
	
	shipTypes = list(NUM_OF_SHIPS_ON_BOARD.keys())
	shipNumbers = list(NUM_OF_SHIPS_ON_BOARD.values())
	

	for ship in range(len(shipTypes)):
		newBoard = deployShip(board, shipTypes[ship], shipNumbers[ship], ships_on_board)
	
	return newBoard

def deployShip(board, shipType, numOfShips, deployedShips):
	
	shipLength = SHIP_LENGTHS[shipType]
	
	if shipType == 'admiral':
		shipMark = 'a'
	elif shipType == 'cruiser':
		shipMark = 'c'
	elif shipType == 'destroyer':
		shipMark = 'd'
	elif shipType == 'submarine':
		shipMark = 's'
	
	ship = []
	emptyCells = []
	
	for shipNumber in range(numOfShips):
		direction = random.randint(0,1)
		if direction == 0:
			shipDirection = 'X'
		else:
			shipDirection = 'Y'
		
		if shipDirection == 'X':
			while True:
				cellX = random.randint(0,10 - shipLength)
				cellY = random.randint(0,10 - shipLength)
				
				#shipCells = []
				
				isStartPointsValid = True
				for i in range(shipLength):
					if board[(cellX+i, cellY)] != EMPTY_SPACE:
						isStartPointsValid = False
						
					#shipCells.append((cellX+i,cellY))
				
				if isStartPointsValid:
					startX = cellX
					startY = cellY
					break
					
			for shipIndex in range(shipLength):
				ship.append((startX+shipIndex,startY))
				
				emptyCells.append((startX-1,startY))
				emptyCells.append((startX+shipLength, startY))
				for i in range(shipLength):
					emptyCells.append((startX+i, startY-1))
					emptyCells.append((startX+i, startY+1))
			
			print(emptyCells)
			
			
		elif shipDirection == 'Y':
			while True:
				cellX = random.randint(0,10 - shipLength)
				cellY = random.randint(0,10 - shipLength)
			
				#shipCells = []
				
				isStartPointsValid = True
				for i in range(shipLength):
					if board[(cellX, cellY+i)] != EMPTY_SPACE:
						isStartPointsValid = False
						
					#shipCells.append((cellX,cellY+i))
			
				if isStartPointsValid:
					startX = cellX
					startY = cellY
					break
					
			for shipIndex in range(shipLength):
				ship.append((startX,startY+shipIndex))
				
		for y in range(10):
			for x in range(10):
				if (x, y) in ship:
					board[(x, y)] = shipMark
					deployedShips[(x, y)] = shipMark
					
	return board
	
def getEmptyCellsAroundShips(emptyCells, colomnIndex, rowIndex, lenght):
	pass


def displayBoard(board):
	gridChars = []
	for rowIndex in range(10):
	    for colomnIndex in range(10):
	        gridChars.append(board[(colomnIndex, rowIndex)])
	
	print(BOARD_TEMPLATE.format(*gridChars))

def getPlayerMove(board):

    print("Please select your target or (Q)uit.")
    while True:  # Keep asking player until they enter a valid move.
        response = input("> ").upper().strip()

        if response.startswith("Q"):
            print("Thanks for playing!")
            input("Press ENTER to exit.")
            sys.exit()

        if not (2<=len(response)<=3):
            print("Please use this format when you select your target : J3 or c10")
            continue  # Ask player again for their move.
	
        if not response[0] in BOARD_COLOMN_LABELS:
            print("Your target must start with a valid letter (ie. from A to J)")
            continue  # Ask player again for their move.
            
        if len(response) == 2:
	        if not response[1] in BOARD_ROW_LABELS:
	            print("Your target must end with a valid number (ie. from 1 to 10)")
	            continue  # Ask player again for their move.
        elif len(response) == 3:
        	if not response[1:] == BOARD_ROW_LABELS[-1]:
	            print("Your target must end with a valid number (ie. from 1 to 10)")
	            continue  # Ask player again for their move.
	
        # Rename colomn and row for easy use.
        targetRow = int(response[1:]) - 1
        targetColomn = BOARD_COLOMN_LABELS.index(response[0])
        target = (targetColomn, targetRow)

        if board[target] != EMPTY_SPACE:
            print("Please select an empty cell")
            continue  # Ask player again for their move.

        return target

def makePlayerMove(board, target, ships):
	
	if target in ships:
		board[(target)] = 'O'
	else:
		board[(target)] = 'X'
	
	return board

main()