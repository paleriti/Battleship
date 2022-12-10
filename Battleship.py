"""Game:Battleship, by Yasar Murat, yasarmurat@msn.com

A strategy type guessing game for single player or against computer.
"""

import random, sys, time

# Constants used for displaying the board:
BOARD_COLOMN_LABELS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
X_MAX = len(BOARD_COLOMN_LABELS)-1 # The maximum number that can be used as colomn number
BOARD_ROW_LABELS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
Y_MAX = len(BOARD_ROW_LABELS)-1 # The maximum number that can be used as row number
assert len(BOARD_COLOMN_LABELS) == len(BOARD_ROW_LABELS)
# Don't forget to update BOARD_TEMPLATE if number of colomn or row labels are changed.

EMPTY_SPACE = ' '
OCEAN_MARK = '~'
SHIP_MARK = '#' # Used when creating a new board.
SHOTS_HIT = 'O' # Used while playing the game.
SHOTS_MISSED = '-' # # Used while playing the game.
SHOTS_PER_TURN = 1 # Can be changed for different game experiences.
SIMULATION_SIZE = 100 # The number of times the computer conducts a simulation.
 
# The types and the numbers of the ships deployed on the board. ( Can be changed for different game experiences)
NUM_OF_SHIPS_ON_BOARD = {'admiral': 1, 'cruiser': 2, 'destroyer': 3, 'submarine': 4}
# The number of squares for each ship is determined by the type of ship. # The ships cannot overlap.
SHIP_LENGTHS = {'admiral': 5, 'cruiser': 4, 'destroyer': 3, 'submarine': 2}

# The string for displaying the board:
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
     ---------------------"""

def singlePlayer():
	""" This function is used if the player chooses single player.
	There is only one board and the player tries to find all the ships by making shots.
	"""

	# Prapere the board first with ships and later without them to display. 
	# 'deployedShips' is used for tracking the hits.
	boardWithShips = boardSetup()
	boardWithoutShips, deployedShips = getBoardWithoutShips(boardWithShips)
	
	turnCount = 1
	while True: # Run player's turn.

		# Clears the screen before displaying the board
		print("\033[H\033[J", end="") 
		
		# Display the board:
		displayBoard(boardWithoutShips)
		print()
		print(f'This is your {turnCount}. shot')
		
		# Get player move
		playerTargets = getPlayerMove(boardWithoutShips)
	
		# Make the move and update the game board accordingly
		makeTheMove(boardWithoutShips, playerTargets, deployedShips)
		
		# Check if there is a winner 
		if isComplete(boardWithoutShips, deployedShips):
			print("\033[H\033[J", end="") # Clear the screen.
			displayBoard(boardWithoutShips) # Display the board one last time.
			print('Congrats, you hit all the ships!')
			input('Press ENTER to exit')
			sys.exit()
		
		turnCount += 1
		
def boardSetup():
	"""Prepares a new board for game play and returns a dictionary that represents a new battleship board."""
	
	# Prapere an empty board
	emptyBoard = {}
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			emptyBoard[(colomn, row)] = EMPTY_SPACE
	
	# Deploy the ships using empty board.
	boardWithShips = getNewBoard(emptyBoard)
	
	return boardWithShips
	
def getNewBoard(board):
	""" Returns a dictionary that represents a new 2048 board.
	The keys are (columnIndex, rowIndex) tuples of two integers and the values are '2's and empty space strings.
	"""
	
	# Get the ships that will be used on the board and their corresponding numbers to gererate a new board.
	shipTypes = list(NUM_OF_SHIPS_ON_BOARD.keys())
	numberOfShipsPerType = list(NUM_OF_SHIPS_ON_BOARD.values())
	
	typeCounter = 0
	while typeCounter < len(shipTypes): # Make sure each type of ship is deployed properly.
		
		newBoard, retryCounter = deployShip(board, shipTypes[typeCounter], numberOfShipsPerType[typeCounter])
		
		# Go to next type of ship to deploy it.
		typeCounter += 1

		# if deployShip function cannot deploy any more ships, reset the whole board to start over.
		if retryCounter == 1000:
			for row in range(len(BOARD_ROW_LABELS)):
				for colomn in range(len(BOARD_COLOMN_LABELS)):
					board[(colomn, row)] = EMPTY_SPACE
			typeCounter = 0
			continue
	
	# Replace the ocean mark to empty space for a better display.
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			if newBoard[(colomn, row)] == OCEAN_MARK:
				newBoard[(colomn, row)] = EMPTY_SPACE
	
	return newBoard
	
def deployShip(board, shipType, numOfShipsPerShipType):
	""" Takes the type of ship (e.g. admiral) and its corresponding number as parameter
	and returns a board with the ship deployed.	"""
	
	# Get the number of grids that must be filled according to the type of ship and its lenght.
	shipLength = SHIP_LENGTHS[shipType]
		
	shipCells = [] 
	oceanCells = []

	for shipIndex in range(numOfShipsPerShipType):
		
		resetCounter = 0 # Used to prevent the game going into infinite loop.

		# Each ship can be deployed horizontally or vertically and this is decided randomly.
		direction = random.randint(0,1) 
		if direction == 0:
			shipDirection = 'X'
		else:
			shipDirection = 'Y'
			
		if shipDirection == 'X':
			while True:
				# Keep trying to find a valid starting point to deploy the ship.

				# CellX and CellY are possible starting points of the ship. 
				cellX = random.randint(0, len(BOARD_COLOMN_LABELS) - shipLength)  
				cellY = random.randint(0, len(BOARD_ROW_LABELS) - shipLength) 
				
				# Make sure the ships don't overlap
				isStartPointsValid = True
				for i in range(shipLength):
					if board[(cellX + i, cellY)] != EMPTY_SPACE:
						isStartPointsValid = False
						
				resetCounter += 1
				if resetCounter == 1000:
					return board, resetCounter # Return the board to start over. 
					
				# startX and startY are valid starting points of the ship.
				if isStartPointsValid:
					startX = cellX
					startY = cellY
					break
					
			for i in range(shipLength):
				# Deploy the ship.
				shipCells.append((startX + i, startY))
				
				# Mark the ocean since there must always be ocean between ships.
				if startX >= 0:
					oceanCells.append((startX - 1, startY))
					oceanCells.append((startX + shipLength, startY))
				if startY >= 0:
					for j in range(shipLength + 2):
						oceanCells.append((startX + j-1, startY - 1))
						oceanCells.append((startX + j-1, startY + 1))
			
			
		elif shipDirection == 'Y':
			while True: # Keep trying to find a valid starting point to deploy the ship.

				# CellX and CellY are possible starting points of the ship
				cellX = random.randint(0, len(BOARD_COLOMN_LABELS) - shipLength)
				cellY = random.randint(0, len(BOARD_ROW_LABELS) - shipLength)
				
				# Make sure the ships don't overlap
				isStartPointsValid = True
				for i in range(shipLength):
					if board[(cellX, cellY + i)] != EMPTY_SPACE:
						isStartPointsValid = False
			
				resetCounter += 1
				if resetCounter == 1000:
					return board, resetCounter # Return the board to start over.
				
				# startX and startY are valid starting points of the ship.
				if isStartPointsValid:
					startX = cellX
					startY = cellY
					break
					
			for i in range(shipLength):
				# Deploy the ship.
				shipCells.append((startX, startY + i))
				
				# Mark the ocean since there must always be ocean between ships.
				if startX >= 0:
					oceanCells.append((startX, startY - 1))
					oceanCells.append((startX, startY + shipLength))
				if startY >= 0:
					for j in range(shipLength + 2):
						oceanCells.append((startX - 1, startY + j-1))
						oceanCells.append((startX + 1, startY + j-1))	
				
		# Replace the EMPTY_SPACE with SHIP_MARK and OCEAN_MARK accordingly
		for row in range(len(BOARD_ROW_LABELS)):
			for colomn in range(len(BOARD_COLOMN_LABELS)):
				if (colomn, row) in shipCells:
					board[(colomn, row)] = SHIP_MARK
				if (colomn, row) in oceanCells:
					board[(colomn, row)] = OCEAN_MARK
		
		shipIndex += 1
				
	return board, resetCounter

def displayBoard(board):
	""" Displays the board and its cells on the screen.

	Prepares a list to pass to the format() string method for the board template.
	The list holds all of the board's marks and empty spaces, going left to right, top to bottom.
	"""
	
	gridChars = []
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			gridChars.append(board[(colomn, row)])
	
	print(BOARD_TEMPLATE.format(*gridChars))

def getBoardWithoutShips(board):
	""" Gets the ship positions from the board and returns as a seperate list along with a new empty board.	"""
	
	emptyBoard = {}
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			emptyBoard[(colomn, row)] = EMPTY_SPACE
	
	deployedShip = []
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			if board[(colomn, row)] == SHIP_MARK:
				deployedShip.append((colomn, row))
				
	return emptyBoard, deployedShip

def getPlayerMove(board):
	"""Let the player select a grid to make a shot.	Returns a list of targets according to SHOTS_PER_TURN """

	targets = []

	# Count the empty spaces on the board.
	emptySpaces = 0
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			if board[(colomn, row)] == EMPTY_SPACE:
				emptySpaces += 1

	moveCounter = 0
	while emptySpaces > moveCounter:
		# Ensures a continues game play if the SHOTS_PER_TURN is set more than 1.
		if moveCounter == SHOTS_PER_TURN:
			break
		moveCounter += 1
		
		if SHOTS_PER_TURN == 1:
			print("Please select your target or (Q)uit.")
		else:
			print(f"Please select your {moveCounter}. target or (Q)uit.")

		while True:  # Keep asking player until they enter a valid move.
		
			response = input("> ").upper().strip()

			if response.startswith("Q"):
				print("Thanks for playing!")
				input("Press ENTER to exit.")
				sys.exit()

			if not (2 <= len(response) <= 3):
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
				print("Your target is already shot!")
				continue  # Ask player again for their move.

			if target in targets:
				print(f"You already selected that target : {response}")
				continue # Ask player again for their move.

			else:
				targets.append(target)
				break

	return targets

def makeTheMove(board, targets, ships):
	""" Changes the board grids as a hit mark or a missed mark """
	
	hitSuccessful = False # If the player hit a ship they can shot again. 

	for i in range(len(targets)):
		if targets[i] in ships:

			# Change the board with a hit mark
			board[(targets[i])] = SHOTS_HIT
			hitSuccessful = True
			
			# Change the board so that the surrounding of the ship is marked with a missed mark
			x = targets[i][0]
			y = targets[i][1]
			board[(x - 1, y - 1)] = SHOTS_MISSED
			board[(x - 1, y + 1)] = SHOTS_MISSED
			board[(x + 1, y - 1)] = SHOTS_MISSED
			board[(x + 1, y + 1)] = SHOTS_MISSED
			
		else:
			board[(targets[i])] = SHOTS_MISSED
	
	return board, hitSuccessful
	
def isComplete(board, allShips):
	""" Checks whether all the ships on the board are hit."""
	
	isAllHit = False
	numberOfHits = 0

	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			if board[(colomn, row)] == SHOTS_HIT:
				numberOfHits += 1
	
	if numberOfHits == len(allShips):
		isAllHit = True
		
	return isAllHit
	
def playAgainstComputer():
	""" This function is used if the player chooses 'Play Against Computer'.
	There are two boards (one for player, one for computer) and each one tries to hit opponent's all ships.
	"""
	
	turn = whoGoesFirst() # Decide who plays first randomly.
	if turn == 'player':
		print('You will go first.')
	else:
		print('The computer will go first.')
	
	# Before game start computer conducts a simulation and makes its moves according to it.
	simulationResult = simulation() 
	print('Loading...') # Ask player to wait until simulation is complete.

	# Prepare both player's and computer's boards.
	playerBoardWithShips = boardSetup()
	playerBoardWithoutShips, playerDeployedShips = getBoardWithoutShips(playerBoardWithShips)
	computerBoardWithShips = boardSetup()
	computerBoardWithoutShips, computerDeployedShips = getBoardWithoutShips(computerBoardWithShips)
	
	while True: # Runs each turn (player or computer)

		# Clears the screen before displaying the board
		print("\033[H\033[J", end="") 
		
		# Display player's and computer's boards.
		displayBoard(playerBoardWithoutShips)
		print("        Player's Board")
		displayBoard(computerBoardWithoutShips)
		print("        Computer's Board")
		print()
		
		if turn == 'player' :
	
			# Gets player's move based on computer's board.
			playerTargets = getPlayerMove(computerBoardWithoutShips)
			
			# Make player's move and change the board accordingly.
			computerBoardWithoutShips, hitSuccessful = \
				makeTheMove(computerBoardWithoutShips, playerTargets, computerDeployedShips)
			
			if isComplete(computerBoardWithoutShips, computerDeployedShips):
				print("\033[H\033[J", end="") # Clear the screen to display the result.
				
				# Display the boards one last time.
				displayBoard(playerBoardWithoutShips)
				print("        Player's Board")
				displayBoard(computerBoardWithoutShips)
				print("        Computer's Board")
				print()
				
				print('WELL DONE! You hit all the ships!')
				input('Press ENTER to exit')
				sys.exit()

			# if the player (or computer) makes a successful hit they continue to shoot.
			elif hitSuccessful:
				turn = 'player'
			else:
				turn = 'computer'
		
		elif turn == 'computer':

			# Get computer move according to simulation result.
			computerTargets = getComputerMove(playerBoardWithoutShips, simulationResult)
			
			print('Computer is making its move...')
			time.sleep(1) # Since the computer makes the move too fast, wait 1 sec for the player to see the move.
			
			# Make the computer's move and change the board accordingly.
			playerBoardWithoutShips, hitSuccessful = \
				makeTheMove(playerBoardWithoutShips, computerTargets, playerDeployedShips)
			
			if isComplete(playerBoardWithoutShips, playerDeployedShips):
				print('TOO BAD! You lost all your ships!')
				input('Press ENTER to exit')
				sys.exit()

			# if the player (or computer) makes a successful hit they continue to shoot.
			elif hitSuccessful:
				turn = 'computer'
			else:
				turn = 'player'
			
def getComputerMove(board, simResult):
	""" Takes the simulation result and current board as parameter and decides where to make the next move """
	
	# Add all the simulation results to a list for later use.
	possibleSimTargets = []
	for i in range(len(simResult)):
		possibleSimTargets.append(simResult[i][0])
	
	possibleTargets = []
	
	# Set all directions to None so we can compare it with EMPTY_SPACE
	left = None
	right = None
	up = None
	down = None
	
	# Decide where to make the next move if computer finds a hit ship. 
	# Add all possible positions to possibleTargets list 
	for y in range(len(BOARD_ROW_LABELS)):
		for x in range(len(BOARD_COLOMN_LABELS)):
			if board[(x, y)] == SHOTS_HIT:
				# It checks all possible positions one by one and changes the direction from 'None' to that position.
				
				if x == 0:
					if y == 0: # The ship mark is on top-left corner.
						down = board[(x, y+1)]
						right = board[(x+1, y)]
					if y > 0 and y < Y_MAX :
						up = board[(x, y-1)]
						down = board[(x, y+1)]
						right = board[(x+1, y)]
					if y == Y_MAX: # The ship mark is on bottom-left corner.
						right = board[(x+1, y)]
						up = board[(x, y-1)]
				
				if x == X_MAX:
					if y > 0 and y < Y_MAX:
						up = board[(x, y-1)]
						down = board[(x, y+1)]
						left = board[(x-1, y)]
					if y == Y_MAX : # The ship mark is on bottom-right corner.
						up = board[(x, y-1)]
						left = board[(x-1, y)]
				
				if y == 0:
					if x > 0 and x < X_MAX:
						down = board[(x, y+1)] 
						right = board[(x+1, y)]
						left = board[(x-1, y)]
					if x == X_MAX: # The ship mark is on top-right corner.
						left = board[(x-1, y)]
						down = board[(x, y+1)]
						
				if y == Y_MAX :
					if x > 0 and x < X_MAX:
						left = board[(x-1, y)]
						right = board[(x+1, y)]
						up = board[(x, y-1)]
				
				if x > 0 and x < X_MAX and y > 0 and y < Y_MAX:
					left = board[(x-1, y)]
					right = board[(x+1, y)]
					up = board[(x, y-1)]
					down = board[(x, y+1)]
					
				# Check whether left, right, top or bottom is empty.
				if left == EMPTY_SPACE:
					possibleTargets.append((x-1, y))
				if right == EMPTY_SPACE:
					possibleTargets.append((x+1, y))
				if up == EMPTY_SPACE:
					possibleTargets.append((x, y-1))
				if down == EMPTY_SPACE:
					possibleTargets.append((x, y+1))

	# Add the simulation result to possibleTargets list.
	# We account the simulation result last so as to possibly select a grid of an unsunk ship first.
	for i in range(len(simResult)):
		if board[possibleSimTargets[i]] == EMPTY_SPACE and (possibleSimTargets[i] not in possibleTargets):
			possibleTargets.append(possibleSimTargets[i])

	targets = []
	for i in range(SHOTS_PER_TURN):
		targets.append(possibleTargets[i])
	
	return targets

def whoGoesFirst():
	""" Randomly choose which player goes first."""

	if random.randint(0, 1) == 0:
		return 'player'
	else:
		return 'computer'

def simulation():
	""" Generates the board a certain number of times (SIMULATION_SIZE) 
	and counts the ship marks in which position it's been seen.
	
	Sorts the result from big to small and retuns a dictionary 
	with the greatest possible position of a ship being the first to appear.
	"""
	
	simBoard = {}
	for row in range(len(BOARD_ROW_LABELS)):
		for colomn in range(len(BOARD_COLOMN_LABELS)):
			simBoard[(colomn, row)] = 0
	
	# Count the ship marks 
	for i in range(SIMULATION_SIZE):
		board = boardSetup()
		for row in range(len(BOARD_ROW_LABELS)):
			for colomn in range(len(BOARD_COLOMN_LABELS)):
				if board[(colomn,row)] == SHIP_MARK:
					simBoard[(colomn,row)] += 1
	
	# Sorts the simBoard values from big to small.
	simResult = sorted(simBoard.items(), key=lambda x: x[1], reverse=True)
	
	return simResult

def main():
	"""Runs a single game of Battleship."""

	print('Please choose : (S)ingle Player or Against (C)omputer?')
	
	while True: # Keep asking until the user gives a valid response.
		response = input().upper().strip()

		if response.startswith('S'):
			singlePlayer()
			break
		elif response.startswith('C'):
			playAgainstComputer()
			break
		else:
			print('Please choose : (S)ingle Player or Against (C)omputer?')

#  If this program was run (instead of imported), run the game:
if __name__ == "__main__":
    main()
	