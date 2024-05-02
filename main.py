#						tic tc toe with Minimax algorithm implementation, By: Lu
##################################################################################################################################
# I'm not gonna lie, the reference code for the Minimax algorith I got it from here: https://www.youtube.com/watch?v=trKjYdBASyQ #
# after taking a look at the coding challage video, it helped me understand how this algorithm is implemented in tic tac toe     #
# so I made my own version of it, because I have nothing better to do,                                                           #
# either way, I hope this project helps you understand how to use Pygame without so much fuzz                                    #
##################################################################################################################################

import pygame
from time import sleep
import math
from colors import*

pygame.init()
pygame.display.set_caption("Minimax Tic Tac Toe By: Lu")

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

play_area_width = 400
play_area_height = 400
cell_width = play_area_width // 3
cell_height = play_area_height // 3

# this field is behind the green grid, it helps to determine on wich cell the mouse is at
# change the fill to 0 if the play area annoys you
play_field = pygame.Surface((play_area_width,play_area_height))
play_field.fill(dark_grey)


matrix = [['','',''],
		  ['','',''],
		  ['','','']]

# prints the 2d array in the console
def printData(matrix):
	for i in range(3):
		for j in range(3):
			print(matrix[i][j], ' ', end = '')
		print("\n")

# draws the green grid
def displayGrid(window):
	pygame.draw.line(window, green, (cell_width * 2, 0), (cell_width * 2, play_area_height), 10)
	pygame.draw.line(window, green, (cell_width * 3, 0), (cell_width * 3, play_area_height), 10)

	pygame.draw.line(window, green, (cell_width, cell_height), (cell_width * 4, cell_height), 10)
	pygame.draw.line(window, green, (cell_width, cell_height * 2), (cell_width * 4, cell_height * 2), 10)

# draws the sprite of the X's or O's acording to the data in the 2d array
def drawOnBoard(window, X, O):
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == 'X':
				window.blit(X, (cell_width + (cell_width) * j + 20, cell_height * i))
			elif matrix[i][j] == 'O':
				window.blit(O, (cell_width + (cell_width) * j + 20, cell_height * i))

# when either the player or the ai play a move, it get's stored in the 2d array
def drawOnMatrix(x, y, player_turn):
	column = x - 1
	row = y - 1
	last_turn = player_turn

	if matrix[row][column] == '':
		if player_turn:
			matrix[row][column] = 'X'
			player_turn = False
			return player_turn
		if not player_turn:
			matrix[row][column] = 'O'
			player_turn = True
			return player_turn
	else:
		return last_turn

def checkWiner():
	winner = ''
	for i in range(3):
		# vertical
		if matrix[i][0] == 'X' and matrix[i][1] == 'X' and matrix[i][2] == 'X': winner = 'X'
		# horizontal
		elif matrix[0][i] == 'X' and matrix[1][i] == 'X' and matrix[2][i] == 'X': winner = 'X'

		#diagonal
		if matrix[0][0] == 'X' and matrix[1][1] == 'X' and matrix[2][2] == 'X': winner = 'X'
		elif matrix[2][0] == 'X' and matrix[1][1] == 'X' and matrix[0][2] == 'X': winner = 'X'


		# vertical
		if matrix[i][0] == 'O' and matrix[i][1] == 'O' and matrix[i][2] == 'O': winner = 'O'
		# horizontal
		elif matrix[0][i] == 'O' and matrix[1][i] == 'O' and matrix[2][i] == 'O': winner = 'O'

		#diagonal
		if matrix[0][0] == 'O' and matrix[1][1] == 'O' and matrix[2][2] == 'O': winner = 'O'
		elif matrix[2][0] == 'O' and matrix[1][1] == 'O' and matrix[0][2] == 'O': winner = 'O'

	open_spaces = 0
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == '':
				open_spaces += 1

	if winner == '' and open_spaces == 0:
		return "tie"
	else:
		return winner

# collision detection for the mouse and replay button
def checkCollision(x, y, otherX, otherY, otherW, otherH):
	if x < otherX or x > otherX + otherW: return False
	elif y < otherY or y > otherY + otherH: return False
	else: return True

# Minimax Algorithm
def minimax(matrix, isMaximizing):
	winner = checkWiner()
	if winner == 'X': return -1
	if winner == 'O': return 1
	if winner == "tie": return 0

	if isMaximizing:
		best_score = -1

		for i in range(3):
			for j in range(3):
				if matrix[i][j] == '':
					matrix[i][j] = 'O'
					score = minimax(matrix, False)
					matrix[i][j] = ''
					best_score = max(score, best_score)
					print("MAX ", best_score)
					printData(matrix)
		return best_score

	else:
		best_score = 1

		for i in range(3):
			for j in range(3):
				if matrix[i][j] == '':
					matrix[i][j] = 'X'
					score = minimax(matrix, True)
					matrix[i][j] = ''
					best_score = min(score, best_score)
					print("min ", best_score)
					printData(matrix)
		return best_score

# ai move
def aiPlayMove():
	best_score = -1

	for i in range(3):
		for j in range(3):
			if matrix[i][j] == '':
				matrix[i][j] = 'O'
				score = minimax(matrix, False)
				matrix[i][j] = ''

				if score > best_score:
					matrix[i][j] = 'O'
					player_turn = True
					return player_turn

# game progress values
player_turn = True
running = True
final_winner = ''
game_over = False

# play again button values
button = pygame.Surface((100,50))
button.fill(dark_blue)
mouse_on_button = False
button_coordinates = [cell_width * 3 + 10, cell_height * 3 + 10]

while running:

	# ai implementation
	if not player_turn:
		player_turn = aiPlayMove()

	# get the mouse pos
	MP = pygame.mouse.get_pos()

	# translate the mouse pos to represent coordinates in the playing field
	mouseX = MP[0] // cell_width
	mouseY = MP[1] // cell_width + 1

	# events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# detect click event, but prevent from calling the function if mouse is not within playing area
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mouseX > 0 and mouseX < 4:
				if mouseY > 0 and mouseY < 4:
					if not game_over:
						player_turn = drawOnMatrix(mouseX, mouseY, player_turn)

			# replay button clicked
			if mouse_on_button and game_over:
				matrix = [['','',''],
						  ['','',''],
						  ['','','']]
				game_over = False

	# fonts
	X = pygame.font.SysFont("dejavusans", cell_width, bold=True)
	X = X.render("X", True, red)
	O = pygame.font.SysFont("dejavusans", cell_width, bold=True)
	O = O.render("O", True, cyan)

	turn = pygame.font.SysFont("dejavusans", cell_width // 2, bold=True)

	if player_turn and final_winner == '': turn = turn.render("X's turn", True, red)
	if not player_turn and final_winner == '': turn = turn.render("O's turn", True, cyan)
	if final_winner == 'X': turn = turn.render("X wins!", True, red)
	elif final_winner == 'O': turn = turn.render("O wins!", True, cyan)
	elif final_winner == "tie": turn = turn.render("TIE!!", True, purple)

	button_font = pygame.font.SysFont("dejavusans", 14, bold=True)
	button_font = button_font.render("Play again?", True, green)

	# check who will win
	final_winner = checkWiner()
	if final_winner == 'X' or final_winner == 'O' or final_winner == "tie":
		game_over = True


	# RENDER
	window.fill(0)

	window.blit(play_field, (cell_width,0))
	displayGrid(window)
	drawOnBoard(window, X, O)

	window.blit(turn, (cell_width,cell_height * 3))

	if game_over:
		window.blit(button, button_coordinates)
		window.blit(button_font, (cell_width * 3 + 20, cell_height * 3 + 20))

	if checkCollision(MP[0], MP[1], button_coordinates[0], button_coordinates[1], 100, 50):
		button.fill(purple)
		mouse_on_button = True
	else:
		button.fill(dark_blue)
		mouse_on_button = False

	pygame.display.update()
	sleep(10/1000)

quit()

