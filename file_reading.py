# ______________________________________________________________________________________________________________________
#  libraries
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- standard libraries ---------------------------------------------------------------------------------------------
from dataclasses import dataclass
from pathlib import Path
import json
import sys
import math

from typing import List, Tuple, Dict
from enum import Enum

# ----- custom libraries -----------------------------------------------------------------------------------------------
# import util

# ______________________________________________________________________________________________________________________
#  constants
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾


# ______________________________________________________________________________________________________________________
#  types declaration
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
class SeatType(Enum):
	UnavailableCell = '#'
	DeveloperDesk = '_'
	ProjectManagerDesk = 'M'


# ______________________________________________________________________________________________________________________
#  classes
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#@dataclass
class Developer(object):
	company: str
	bonus: list
	skill_size: int
	skills: list
	seat_line: int
	seat_column: int
	
	def __init__(self, width: int = -1, height: int = -1, seats: List[List[Tuple[SeatType, bool]]] = [[]]):
		self.width = width
		self.height = height
		self.seats = seats
	
#@dataclass
class ProjectManager(object):
	company: str
	bonus: list
	seat_line: int
	seat_column: int
	
#@dataclass
class OfficeFloor(object):
	width: int
	height: int
	seats: List[List[Tuple[SeatType, bool]]]  # matrix where each cell is a pair (type, is_filled)
	
	def __init__(self, width: int = -1, height: int = -1, seats: List[List[Tuple[SeatType, bool]]] = [[]]):
		self.width = width
		self.height = height
		self.seats = seats


# ______________________________________________________________________________________________________________________
#  global variables
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
#----- paths ------
path_input: Path = Path.cwd()
path_output: Path = Path.cwd()

#----- data base -----
floor: OfficeFloor
developers: List[Developer]
dev_per_company: Dict[str, List[Developer]]
managers: List[ProjectManager]


# ______________________________________________________________________________________________________________________
#  functions
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def read(path_input: Path):
	# check input type
	if type(path_input) == str:
		path_input = Path(path_input)
	
	# open file
	with path_input.open('r') as file:
		#----- seat disposition -----
		# read W and H
		first_line: str = file.readline()
		w = first_line.split(' ')[0]
		h = first_line.split(' ')[1]
		
		global floor
		floor = OfficeFloor()
		floor.width = int(w)
		floor.height = int(h)
		
		# read map
		floor.seats = [None] * floor.height
		for line in range(0, floor.height):
			floor.seats[line] = [None] * floor.width
			for column in range(0, floor.width):
				char: str = file.read(1)
				seat = SeatType(char)
				floor.seats[line][column] = (seat, False)  # is_filled initialized as empty
			file.read(1)  # discard \n

		#----- developers -----
		# read dev number
		dev_num = int(file.readline())
		developers = [None] * dev_num
		dev_per_company = {}
		
		# read developer details
		for i in range(0, dev_num):
			line: str = file.readline()
			fields: list = line.split(' ')
			
			dev: Developer = Developer()
			dev.company = fields[0]
			dev.bonus = fields[1]
			dev.seat_line = -1  # initialized as invalid index
			dev.seat_column = -1  # initialized as invalid index
			
			skill_size: int = int(fields[2])
			dev.skills = [None] * skill_size
			for j in range(0, skill_size):
				dev.skills.append(fields[i+j])
			
			# insert developer in database
			developers.append(dev)
			if dev.company not in dev_per_company:
				dev_per_company[dev.company] = []
			dev_per_company[dev.company].append(dev)

		#----- project managers -----
		
