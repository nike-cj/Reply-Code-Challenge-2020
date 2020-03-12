# ______________________________________________________________________________________________________________________
#  libraries
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- standard libraries ---------------------------------------------------------------------------------------------
import getopt
from pathlib import Path
import json
import sys

from typing import List, Tuple
from enum import Enum

# ----- custom libraries -----------------------------------------------------------------------------------------------
import file_reading
from utils import *

# ______________________________________________________________________________________________________________________
#  constants
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾


# ______________________________________________________________________________________________________________________
#  global variables
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾



# ______________________________________________________________________________________________________________________
#  types declaration
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾



# ______________________________________________________________________________________________________________________
#  classes
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾



# ______________________________________________________________________________________________________________________
#  functions
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def pickInitialDeveloper():
		for d in file_reading.developers:
			if d.seat_line == -1:
				return d

def recursiveSeatPicker(x: int, y: int, lastDev: file_reading.Developer):
	if lastDev is None:
		# Call function to pick first developer
		dev: file_reading.Developer = pickInitialDeveloper()
	else:
		# Call function to pick next developer
		dev: file_reading.Developer = file_reading.Developer()

	dev.seat_line = x
	dev.seat_line = y
	file_reading.floor.seats[x][y]

	# Check Upper place
	if y > 0:
		if file_reading.floor.seats[x][y-1][0] == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x][y-1][1]:
			recursiveSeatPicker(x, y-1, dev)

	# Check Lower place
	if y < file_reading.floor.height - 1:
		if file_reading.floor.seats[x][y+1][0] == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x][y + 1][1]:
			recursiveSeatPicker(x, y+1, dev)

	# Check Right place
	if x > 0:
		if file_reading.floor.seats[x-1][y][0] == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x -1][y][1]:
			recursiveSeatPicker(x-1, y, dev)

	# Check Left place
	if x < file_reading.floor.width - 1:
		if file_reading.floor.seats[x+1][y][0] == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x+1][y][1]:
			recursiveSeatPicker(x+1, y, dev)

	return

# ______________________________________________________________________________________________________________________
#  main function
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def main(argv):
	# ----- read command line arguments --------------------------------------------------------------------------------
	inputfile: str = 'Input/a_solar.txt'
	outputfile: str = 'output/a.txt'
	try:
		opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
	except getopt.GetoptError:
		print('main.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('main.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print(f'Input file is {inputfile}')
	print(f'Output file is {outputfile}')

	# ----- feed data --------------------------------------------------------------------------------------------------
	file_reading.read(inputfile)

	for x in range(0, file_reading.floor.height):
		for y in range(0, file_reading.floor.width):
			print(x, y)
			if file_reading.floor.seats[x][y][1]:
				continue
			if file_reading.floor.seats[x][y][0] == file_reading.SeatType.UnavailableCell:
				continue
			elif file_reading.floor.seats[x][y][0] == file_reading.SeatType.DeveloperDesk:
				recursiveSeatPicker(x, y, None)
			elif file_reading.floor.seats[x][y][0] == file_reading.SeatType.ProjectManagerDesk:
				pass



# ______________________________________________________________________________________________________________________
#  entry point
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
if __name__ == '__main__':
	try:
		main(sys.argv[1:])
	except Exception as e:
		print(str(e))
	exit(0)
