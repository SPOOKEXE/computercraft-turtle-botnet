
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel

from minecraft import (
	# consts.py
	Direction, Point3, Item,
	Inventory, Block, SolidBlock,
	Chest, Furnace, World
)

class TurtleActions(Enum):
	'''
	Contains all the possible turtle actions.
	'''
	getTurtleInfo = 1

	'''
	Movement actions.
	'''
	forward = 5
	backward = 6
	up = 7
	down = 8
	turnLeft = 9
	turnRight = 10

	'''
	World-interaction actions.
	'''
	attackFront = 20
	attackAbove = 21
	attackBelow = 22
	digFront = 23
	digAbove = 24
	digBelow = 25
	placeFront = 26
	placeAbove = 27
	placeBelow = 28
	detectFront = 29
	detectAbove = 30
	detectBelow = 31
	inspectFront = 32
	inspectAbove = 33
	inspectBelow = 34
	compareFront = 35
	compareAbove = 36
	compareBelow = 37
	dropFront = 38
	dropAbove = 39
	dropBelow = 40
	suckFront = 41
	suckAbove = 42
	suckBelow = 43

	'''
	Inventory management actions.
	'''
	craftItems = 53
	selectSlot = 54
	getSelectedSlot = 55
	getItemCountInSlot = 56
	getItemSpaceInSlot = 57
	getItemDetailsInSlot = 58
	equipLeft = 59
	equipRight = 60
	refuel = 61
	getFuelLevel = 62
	getFuelLimit = 63
	transferTo = 64

	'''
	Customs
	'''
	getDirectionFromSign = 78
	readInventory = 79
	findItemSlotsByPattern = 80
	getEquippedItems = 81
	procreate = 82
	isBusy = 83

class CCTurtle(SolidBlock, Inventory, BaseModel):
	uid : str = uuid4().hex
	name : str = "computercraft:turtle"
	fuel : int = 0
	position : Point3 = Point3()
	direction : Direction = Direction.north
	is_new_turtle : bool = True

	inventory : list = list()
	left_hand : Item = None
	right_hand : Item = None

	queued_jobs : list[list] = list()
	active_job : int = None
	active_args : list = None
	job_results : list | None = None

class CCWorld(World):
	turtles_map : dict[str, CCTurtle] = dict()
	turtle_ids : list[str] = list()
