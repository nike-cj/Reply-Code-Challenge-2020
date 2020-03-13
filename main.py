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
	for d in file_reading.dev_by_bonus:
		if d.seat_line == -1:
			return d

def pickNextDeveloper(dev: file_reading.Developer):
	for v in file_reading.dev_per_company[dev.company]:
		if v.seat_line == -1:
			return v
	return pickInitialDeveloper()

def recursiveSeatPicker(x: int, y: int, lastDev: file_reading.Developer):
	if lastDev is None:
		# Call function to pick first developer
		dev: file_reading.Developer = pickInitialDeveloper()
	else:
		# Call function to pick next developer
		dev: file_reading.Developer = pickNextDeveloper(lastDev)

	dev.seat_line = x
	dev.seat_column = y
	file_reading.floor.seats[x][y].isFilled = True
	file_reading.floor.seats[x][y].owner = dev

	# Check Upper place
	if y > 0:
		if file_reading.floor.seats[x][y-1].type == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x][y-1].isFilled:
			recursiveSeatPicker(x, y-1, dev)

	# Check Lower place
	if y < file_reading.floor.width - 1:
		if file_reading.floor.seats[x][y+1].type == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x][y + 1].isFilled:
			recursiveSeatPicker(x, y+1, dev)

	# Check Right place
	if x > 0:
		if file_reading.floor.seats[x-1][y].type == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x -1][y].isFilled:
			recursiveSeatPicker(x-1, y, dev)

	# Check Left place
	if x < file_reading.floor.height - 1:
		if file_reading.floor.seats[x+1][y].type == file_reading.SeatType.DeveloperDesk and not file_reading.floor.seats[x+1][y].isFilled:
			recursiveSeatPicker(x+1, y, dev)

	return

def pickManager(x: int, y: int):
	list_man = []
	list_score = []

	# Check Upper place
	if y > 0:
		if file_reading.floor.seats[x][y - 1].type != file_reading.SeatType.UnavailableCell and file_reading.floor.seats[x][y - 1].isFilled:
			if file_reading.floor.seats[x][y - 1].owner.company in file_reading.man_per_company:
				for v in file_reading.man_per_company[file_reading.floor.seats[x][y - 1].owner.company]:
					if v.seat_line == -1:
						list_man.append(v)
						break


	# Check Lower place
	if y < file_reading.floor.width - 1:
		if file_reading.floor.seats[x][y + 1].type != file_reading.SeatType.UnavailableCell and file_reading.floor.seats[x][y + 1].isFilled:
			if file_reading.floor.seats[x][y + 1].owner.company in file_reading.man_per_company:
				for v in file_reading.man_per_company[file_reading.floor.seats[x][y + 1].owner.company]:
					if v.seat_line == -1:
						list_man.append(v)
						break

	# Check Right place
	if x > 0:
		if file_reading.floor.seats[x - 1][y].type != file_reading.SeatType.UnavailableCell and file_reading.floor.seats[x - 1][y].isFilled:
			if file_reading.floor.seats[x - 1][y].owner.company in file_reading.man_per_company:
				for v in file_reading.man_per_company[file_reading.floor.seats[x - 1][y].owner.company]:
					if v.seat_line == -1:
						list_man.append(v)
						break

	# Check Left place
	if x < file_reading.floor.height - 1:
		if file_reading.floor.seats[x + 1][y].type != file_reading.SeatType.UnavailableCell and file_reading.floor.seats[x + 1][y].isFilled:
			if file_reading.floor.seats[x + 1][y].owner.company in file_reading.man_per_company:
				for v in file_reading.man_per_company[file_reading.floor.seats[x + 1][y].owner.company]:
					if v.seat_line == -1:
						list_man.append(v)
						break

	if len(list_man) == 0:
		for m in reversed(file_reading.man_by_bonus):
			if m.seat_line == -1:
				file_reading.floor.seats[x][y].isFilled = True
				file_reading.floor.seats[x][y].owner = m
				m.seat_line = x
				m.seat_column = y
				return

	else:
		file_reading.floor.seats[x][y].isFilled = True
		file_reading.floor.seats[x][y].owner = list_man[0]
		list_man[0].seat_line = x
		list_man[0].seat_column = y

	return

# ______________________________________________________________________________________________________________________
#  main function
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def main(argv):
	# ----- read command line arguments --------------------------------------------------------------------------------
	input_file_list = ['Input/a_solar.txt', 'Input/b_dream.txt', 'Input/c_soup.txt', 'Input/d_maelstrom.txt', 'Input/e_igloos.txt', 'Input/f_glitch.txt']
	output_file_list = ['Output/a_solar.txt', 'Output/b_dream.txt', 'Output/c_soup.txt', 'Output/d_maelstrom.txt', 'Output/e_igloos.txt', 'Output/f_glitch.txt']

	sys.setrecursionlimit(200000)

	for i in range(0, 6):
		inputfile: str = input_file_list[i]
		outputfile: str = output_file_list[i]

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
				if file_reading.floor.seats[x][y].isFilled:
					continue
				if file_reading.floor.seats[x][y].type == file_reading.SeatType.UnavailableCell:
					continue
				elif file_reading.floor.seats[x][y].type == file_reading.SeatType.DeveloperDesk:
					recursiveSeatPicker(x, y, None)
				elif file_reading.floor.seats[x][y].type == file_reading.SeatType.ProjectManagerDesk:
					pickManager(x, y)

		file_reading.write(outputfile)


# ______________________________________________________________________________________________________________________
#  entry point
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
if __name__ == '__main__':

	main(sys.argv[1:])
	exit(0)
