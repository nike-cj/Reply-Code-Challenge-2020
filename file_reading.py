# ______________________________________________________________________________________________________________________
#  libraries
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- standard libraries ---------------------------------------------------------------------------------------------
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
class Developer(object):
	company: str
	bonus: list
	skill_size: int
	skills: list
	seat_line: int = -1
	seat_column: int = -1
	
	# def __init__(self, width: int = -1, height: int = -1, seats: List[List[Tuple[SeatType, bool]]] = [[]]):
	# 	self.width = width
	# 	self.height = height
	# 	self.seats = seats
	
class ProjectManager(object):
	company: str
	bonus: list = 0
	seat_line: int = -1
	seat_column: int = -1

class Seat(object):
	type: SeatType
	isFilled: bool

	def __init__(self, type: SeatType, isFilled: bool = False):
		self.type = type
		self.isFilled = isFilled


class OfficeFloor(object):
	width: int
	height: int
	seats: List[List[Seat]]  # matrix where each cell is a pair (type, is_filled)
	
	# def __init__(self, width: int = -1, height: int = -1, seats: List[List[Tuple[SeatType, bool]]] = [[]]):
	# 	self.width = width
	# 	self.height = height
	# 	self.seats = seats

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
dev_by_bonus: List[Developer]
dev_by_num_skills: List[Developer]
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
		# ----- seat disposition -----
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
				seatobj = Seat(seat)
				try:
					floor.seats[line][column] = seatobj  # is_filled initialized as empty
				except Exception as e:
					print(str(e))
			file.read(1)  # discard \n

		# ----- developers -----
		# read dev number
		manager_num = int(file.readline())
		global developers, dev_per_company
		developers = []
		dev_per_company = {}
		
		# read developer details
		for i in range(0, manager_num):
			line: str = file.readline().strip()
			fields: list = line.split(' ')
			
			dev: Developer = Developer()
			dev.company = fields[0]
			dev.bonus = fields[1]
			dev.seat_line = -1  # initialized as invalid index
			dev.seat_column = -1  # initialized as invalid index
			
			dev.skill_size = int(fields[2])
			dev.skills = [None] * dev.skill_size
			for j in range(0, dev.skill_size):
				dev.skills.append(fields[3+j])
			
			# insert developer in database
			developers.append(dev)
			if dev.company not in dev_per_company:
				dev_per_company[dev.company] = []
			dev_per_company[dev.company].append(dev)

		# ----- project managers -----
		# read dev number
		manager_num = int(file.readline())
		global managers
		managers = []
		
		# read developer details
		for i in range(0, manager_num):
			line: str = file.readline().strip()
			fields: list = line.split(' ')
			
			manager: ProjectManager = ProjectManager()
			manager.company = fields[0]
			manager.bonus = fields[1]
			
			# insert project manager in database
			managers.append(manager)

		# ----- sort -----
		for entry in dev_per_company.items():
			key: str = entry[0]
			value: List[Developer] = entry[1]
			value.sort(key=lambda x: x.bonus)
		
		global dev_by_bonus, dev_by_num_skills
		dev_by_bonus = developers.copy()
		dev_by_bonus.sort(key=lambda x: x.bonus, reverse=True)
		
		dev_by_num_skills = developers.copy()
		dev_by_num_skills.sort(key=lambda x: x.skill_size, reverse=True)


def write(path_output: Path):
	# check input type
	if type(path_output) == str:
		path_output = Path(path_output)
		
	# check if missing directory
	path_output.mkdir(exist_ok=True)
	
	# open file
	with path_output.open('w') as file:
		# iterate over developers
		for dev in developers:
			if dev.seat_column == -1 and dev.seat_line == -1:
				file.writelines(f'X\n')
			else:
				file.writelines(f'{dev.seat_line} {dev.seat_column}\n')
		
		# iterate over managers
		for manager in managers:
			if manager.seat_column == -1 and manager.seat_line == -1:
				file.writelines(f'X\n')
			else:
				file.writelines(f'{manager.seat_line} {manager.seat_column}\n')
