from uuid import uuid4
from pydantic import BaseModel
from enum import Enum

class Direction(Enum):
	north = "north"
	south = "south"
	west = "west"
	east = "east"

class Point3(BaseModel):
	x : int = 0
	y : int = 0
	z : int = 0

class Item(BaseModel):
	name : str = 'minecraft:air'
	quantity : int = 0

class Inventory(BaseModel):
	inventory : list[Item] = list()

class Block(BaseModel):
	uid : str = uuid4().hex
	name : str = "minecraft:air"
	position : Point3 = Point3()
	traversible : bool = True

class SolidBlock(Block):
	traversible : bool = False

class Chest(SolidBlock, Inventory, BaseModel):
	name : str = "minecraft:chest"

class Furnace(SolidBlock, Inventory, BaseModel):
	name : str = "minecraft:furnace"

class World(BaseModel):
	uid : str = uuid4().hex
	unique_blocks : list[str] = list()
	block_cache : dict = dict()

	pathfind_cache : dict[str, list] = dict()
