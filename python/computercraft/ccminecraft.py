
import pickle
from minecraft import (
	# consts.py
	Direction, Point3, Item,
	Inventory, Block, SolidBlock,
	Chest, Furnace,
	# world.py
	WorldAPI,
	# recipes.py
)

from .utility import (
	array_find
)

from .consts import (
	CCWorld, CCTurtle, TurtleActions
)

class CCWorldAPI(WorldAPI):

	@staticmethod
	def does_turtle_exist( world : CCWorld, turtle_id : str ) -> bool:
		return array_find( world.turtle_ids, turtle_id ) != -1

	@staticmethod
	def reinitialize_turtle( world : CCWorld, turtle_id : str ) -> None:
		if not CCWorldAPI.does_turtle_exist( world, turtle_id ):
			return
		turtle = world.turtles_map.get( turtle_id )
		if turtle == None:
			return
		turtle.is_new_turtle = True

	@staticmethod
	def create_new_turtle( world : CCWorld, id : str, position : Point3, direction : str ) -> CCTurtle:
		turtle = CCTurtle(uid=id, position=position, direction=direction)
		world.turtle_ids.append(turtle.uid)
		world.turtles_map[turtle.uid] = turtle
		WorldAPI.push_block( world, position, turtle )
		return turtle

	@staticmethod
	def destroy_turtle( world : CCWorld, turtle_id : str ) -> None:
		idx = array_find( world.turtle_ids, turtle_id )
		if idx == -1: return
		world.turtle_ids.pop(idx)

	@staticmethod
	def get_turtle_active_job( world : CCWorld, turtle_id : str ) -> list | None:
		if not CCWorldAPI.does_turtle_exist( world, turtle_id ):
			return None
		turtle = world.turtles_map.get( turtle_id )
		if turtle == None:
			return None
		if turtle.active_job == None:
			return None
		return [ turtle.active_job, *turtle.active_args ]

	@staticmethod
	def set_turtle_job_results( world : CCWorld, turtle_id : str, results : list ) -> None:
		if not CCWorldAPI.does_turtle_exist( world, turtle_id ):
			return None
		turtle = world.turtles_map.get( turtle_id )
		if turtle == None:
			return None
		# set the results
		turtle.job_results = results
		# clear the active job
		turtle.active_job = None
		turtle.active_args = None

	@staticmethod
	def serialize( world : CCWorld ) -> bytes:
		return pickle.dumps( world )

	@staticmethod
	def deserialize( data : bytes ) -> CCWorld:
		return pickle.loads( data )
