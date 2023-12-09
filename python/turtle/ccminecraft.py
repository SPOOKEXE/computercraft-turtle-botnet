
from minecraft import (
	# consts.py
	Direction, Point3, Item,
	Inventory, Block, SolidBlock,
	Chest, Furnace,
	# world.py
	WorldAPI,
	# recipes.py
	RecipeType, RECIPES,
	resolve_recipe_tree, resolve_multi_tree
)

from utility import (
	array_find,
	cache_increment_index,
	cache_push_increment
)

from consts import (
	CCWorld, CCTurtle, TurtleActions
)

class CCWorldAPI(WorldAPI):

	@staticmethod
	def does_turtle_exist( world : CCWorld, turtle_id : str ) -> bool:
		return array_find( world.turtle_ids, turtle_id ) != -1

	@staticmethod
	def create_new_turtle( world : CCWorld, position : Point3, direction : str ) -> CCTurtle:
		turtle = CCTurtle(position=position, direction=direction)
		world.turtle_ids.append(turtle.uid)
		world.turtles_map[turtle.uid] = turtle
		WorldAPI.push_block( world, position, turtle )
		return turtle

	@staticmethod
	def destroy_turtle( world : CCWorld, turtle_id : str ) -> None:
		idx = array_find( world.turtle_ids, turtle_id )
		if idx == -1: return
		world.turtle_ids.pop(idx)

	# @staticmethod
	# def get_turtle_jobs( world : CCWorld, turtle_id : str ) -> list:
	# 	turtle : CCTurtle = world.turtles_map.get(turtle_id)
	# 	if turtle == None: return [ ]
	# 	raise NotImplementedError

	# @staticmethod
	# def put_turtle_results( world : CCWorld, turtle_id : str, tracker_id : str, data : list ) -> None:
	# 	turtle : CCTurtle = world.turtles_map.get(turtle_id)
	# 	if turtle == None: return
	# 	turtle.tracker_results[tracker_id] = data

	@staticmethod
	def update_behavior_trees( world : CCWorld ) -> None:
		raise NotImplementedError
