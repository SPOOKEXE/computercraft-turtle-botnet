
import pickle
from time import sleep

from typing import Any
from uuid import uuid4

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
	def get_turtle_from_id( world : CCWorld, turtle_id : str ) -> CCTurtle | None:
		return world.turtles_map.get( turtle_id )

	@staticmethod
	def reinitialize_turtle( world : CCWorld, turtle_id : str ) -> None:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None: return None
		turtle.is_new_turtle = True

	@staticmethod
	def create_new_turtle( world : CCWorld, id : str, position : Point3, direction : str ) -> CCTurtle:
		turtle = CCTurtle( uid=id, position=position, direction=direction )
		world.turtle_ids.append(turtle.uid)
		world.turtles_map[turtle.uid] = turtle
		WorldAPI.push_block( world, position, turtle )
		return turtle

	@staticmethod
	def destroy_turtle( world : CCWorld, turtle_id : str ) -> None:
		idx = array_find( world.turtle_ids, turtle_id )
		if idx == -1:
			return
		world.turtle_ids.pop(idx)

	@staticmethod
	def get_active_job( world : CCWorld, turtle_id : str ) -> list | None:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None:
			return None
		if turtle.active_job == None:
			return None
		return turtle.job_queue[0]

	@staticmethod
	def set_job_results( world : CCWorld, turtle_id : str, results : list ) -> None:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None:
			return
		active_job : list = turtle.job_queue.pop(0)
		tracker_id : str = active_job.pop(0)
		turtle.tracker_results[ tracker_id ] = results

	@staticmethod
	def yield_turtle_job( world : CCWorld, turtle_id : str, job : int, *args ) -> dict | list | bool:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None:
			return None
		tracker_id : str = uuid4().hex
		turtle.job_queue.append([ tracker_id, job, *args ])
		while turtle.job_queue[0][0] != tracker_id:
			sleep(0.1)
		while turtle.tracker_results.get( tracker_id ) == None:
			sleep(0.1)
		return turtle.tracker_results.pop( tracker_id )

	@staticmethod
	def serialize( world : CCWorld ) -> bytes:
		return pickle.dumps( world )

	@staticmethod
	def deserialize( data : bytes ) -> CCWorld:
		return pickle.loads( data )
