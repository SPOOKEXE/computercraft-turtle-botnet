
from __future__ import annotations

from typing import Any

from consts import Point3, Block, World
from utility import array_find

class WorldAPI:

	@staticmethod
	def get_block( world : World, position : Point3 ) -> Block | None:
		x = str(position.x)
		z = str(position.z)
		y = str(position.y)
		if world.block_cache.get(x) == None:
			return None
		if world.block_cache.get(x).get(z) == None:
			return None
		return world.block_cache[x][z].get(y)

	@staticmethod
	def push_block( world : World, position : Point3, block : Block ) -> bool:
		# cache unique block names
		index = array_find(world.unique_blocks, block.name)
		if index == -1:
			world.unique_blocks.append( [block.uid, block.name] )
			index = len(world.unique_blocks)
		x = str(position.x)
		z = str(position.z)
		y = str(position.y)
		if world.block_cache.get(x) == None:
			world.block_cache[x] = { }
		if world.block_cache.get(x).get(z) == None:
			world.block_cache[x][z] = { }
		world.block_cache[x][z][y] = index

	@staticmethod
	def pop_block( world : World, position : Point3 ) -> None:
		x = str(position.x)
		z = str(position.z)
		y = str(position.y)
		if world.block_cache.get(x) == None: return
		if world.block_cache.get(x).get(z) == None: return
		try: world.block_cache.get(x).get(z).pop(y)
		except: pass

	@staticmethod
	def get_block_neighbours( world : World, source : Point3, allow_diagonals : bool = True, allow_vertical : bool = True, filter_traversible : bool = True ) -> list[Block]:

		leftPlane = source.x - 1
		rightPlane = source.x + 1
		forwardPlane = source.z + 1
		backwardPlane = source.z - 1
		upAxis = source.y + 1
		downAxis = source.y - 1

		def checkNodePath( x : int, z : int, y : int ) -> Block:
			nonlocal world
			position : Point3 = Point3(x=x, y=y, z=z)
			block = WorldAPI.get_block( world, position )
			return block == None and Block(position=position) or block

		neighbour_nodes = [
			checkNodePath( leftPlane, source.z, source.y ), # left-middle-middle
			checkNodePath( rightPlane, source.z, source.y ), # right-middle-middle
			checkNodePath( source.x, forwardPlane, source.y ), # middle-forward-middle
			checkNodePath( source.x, backwardPlane, source.y ), # middle-forward
		]

		if allow_vertical:
			neighbour_nodes.extend([
				checkNodePath( source.x, source.z, upAxis ), # top-middle
				checkNodePath( source.x, source.z, downAxis ) # bottom-middle
			])

		if allow_diagonals:
			neighbour_nodes.extend([
				checkNodePath(leftPlane, forwardPlane, source.y),
				checkNodePath(leftPlane, backwardPlane, source.y),
				checkNodePath(rightPlane, forwardPlane, source.y),
				checkNodePath(rightPlane, backwardPlane, source.y),
			])

		if allow_vertical and allow_diagonals:
			neighbour_nodes.extend([
				checkNodePath(leftPlane, forwardPlane, upAxis),
				checkNodePath(leftPlane, forwardPlane, downAxis),
				checkNodePath(leftPlane, source.z, upAxis),
				checkNodePath(leftPlane, source.z, downAxis),
				checkNodePath(leftPlane, backwardPlane, upAxis),
				checkNodePath(leftPlane, backwardPlane, downAxis),
				checkNodePath(rightPlane, forwardPlane, upAxis),
				checkNodePath(rightPlane, forwardPlane, downAxis),
				checkNodePath(rightPlane, source.z, upAxis),
				checkNodePath(rightPlane, source.z, downAxis),
				checkNodePath(rightPlane, backwardPlane, upAxis),
				checkNodePath(rightPlane, backwardPlane, downAxis),
				checkNodePath(source.x, forwardPlane, upAxis),
				checkNodePath(source.x, forwardPlane, downAxis),
				checkNodePath(source.x, backwardPlane, upAxis),
				checkNodePath(source.x, backwardPlane, downAxis)
			])

		reverse : int = (source.x + source.z + source.y) % 2 == 0
		neighbours : list[Block] = []
		for p in neighbour_nodes:
			if filter_traversible and p.traversible == False:
				continue
			if reverse:
				neighbours.insert(0, p)
			else:
				neighbours.append(p)
		return neighbours

	@staticmethod
	def pathfind3d_to( world : World, start : Point3, goal : Point3 ) -> tuple[bool, list]:
		'''
		Pathfind on the X/Y/Z axis from the start location to the goal location.
		'''
		# A* pathfinding / other method (such as directly going there)

		cacheindex = str(hash( str(start) + str(goal) ))
		if world.pathfind_cache.get( cacheindex ):
			return world.pathfind_cache.get( cacheindex )

		raise NotImplementedError

	@staticmethod
	def on_path_blocked( world : World, path : list[Point3], blockedIndex : int ) -> None:
		raise NotImplementedError
