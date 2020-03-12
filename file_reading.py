# ______________________________________________________________________________________________________________________
#  libraries
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# ----- standard libraries ---------------------------------------------------------------------------------------------
from dataclasses import dataclass
from pathlib import Path
import json
import sys
import math

from typing import List, Tuple
from enum import Enum

# ----- custom libraries -----------------------------------------------------------------------------------------------
# import util

# ______________________________________________________________________________________________________________________
#  constants
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾


# ______________________________________________________________________________________________________________________
#  global variables
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
path_input: Path = Path.cwd()
path_output: Path = Path.cwd()


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
@dataclass
class Developer(object):
	company: str
	bonus: list
	skills: set
	
@dataclass
class ProjectManager(object):
	company: str
	bonus: list
	
class OfficeFloor(object):
	width: int
	height: int
	seats: List[List[SeatType]]


# ______________________________________________________________________________________________________________________
#  functions
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

def read(path_input: Path):
	# local variable
	floor: OfficeFloor = OfficeFloor()
	
	# check input type
	if type(path_input) == str:
		path_input = Path(path_input)
	
	# open file
	with path_input.open('r') as file:
		# read W and H
		first_line: str = file.readline()
		w = first_line.split(' ')[0]
		h = first_line.split(' ')[1]
		
		floor.width = int(w)
		floor.height = int(h)
		
		# read map
		floor.seats = [None] * floor.height
		for line in range(0, floor.height):
			floor.seats[line] = [None] * floor.width
			for column in range(0, floor.width):
				seat = SeatType(file.read(1))
				floor.seats[line][column] = seat

		#----- developers -----
		# read dev number
		dev_num = int(file.read())
		
		# read developer details
		for i in range(0, dev_num):
			line: str = file.readline()
			fields: list = line.split(' ')
			
			dev: Developer = Developer()
			dev.company = fields[0]
			dev.bonus = fields[1]
			
			skill_size: int = int(fields[2])
			dev.skills = [None] * skill_size
			for j in range(0, skill_size):
				dev.skills.append(fields[i+j])
		