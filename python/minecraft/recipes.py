
import pickle
import numpy
import json

from math import ceil

from .utility import ( array_find, cache_increment_index, cache_push_increment )

class ResourceType:
	UNKNOWN = 0
	# natural resources
	SURFACE = 1
	UNDERGROUND = 2
	ORE = 3
	ORE_DROP = 4
	# man-made resources
	CRAFTED = 10
	SMELTED = 11

class RecipeHelpers:

	def construct_craft_recipe( amount : int, *args : str ) -> list[str]:
		recipe = [None] * 9
		for index, value in enumerate(args):
			recipe[index] = value
		return { 'recipe' : recipe, 'amount' : amount}

	def natural_resource( sources : list, blocks : list ) -> dict:
		return { 'sources' : sources, 'blocks' : blocks, 'craft' : None, 'smelt' : None }

	def craftable_resource( recipes : list[list] ) -> dict:
		return { 'sources' : [ ResourceType.CRAFTED ], 'blocks' : None, 'craft' : recipes, 'smelt' : None }

	def smeltable_resource( blocks : list[str] ) -> dict:
		return { 'sources' : [ ResourceType.SMELTED ], 'blocks' : None, 'craft' : None, 'smelt' : blocks }

def count_values( array : list ) -> dict:
	values = { }
	for value in array:
		if value != None and value != 'minecraft:air':
			cache_increment_index( values, value, 1 )
	return values

def resolve_source_id( target : int ) -> str:
	for (name, value) in ResourceType.__dict__.items():
		if name.find('__') == -1 and value == target:
			return name
	return ResourceType.UNKNOWN

class SmartRecipeSystem:

	recipes : dict

	def __init__(self):
		self.recipes = dict()

	def append( self, block_id : str, block_data : dict ) -> None:
		target_block = self.recipes.get(block_id)
		# check if block already exists
		if target_block == None:
			self.recipes[block_id] = block_data
			return

		# print('Block already exists - mutating missing values.')
		# block sources
		for my_source in block_data.get('sources'):
			if array_find( block_data.get('sources'), my_source ) == -1:
				block_data.get('sources').append( my_source )

		# blocks/smelt
		for key in ['blocks', 'smelt']:
			if target_block.get(key) == None and block_data.get(key) != None:
				target_block[key] = block_data[key]
			elif target_block.get(key) != None and block_data.get(key) != None:
				target_block[key].extend( block_data.get(key) )
				target_block[key] = numpy.unique( target_block[key] ).tolist()

		# craft
		if target_block.get('craft') == None and block_data.get('craft') != None:
			target_block['craft'] = block_data['craft']
		elif target_block.get('craft') != None and block_data.get('craft') != None:
			stored_recipes = [ json.dumps(recipe) for recipe in target_block.get('craft') ]
			for recipe in block_data.get('craft'):
				serialized = json.dumps(recipe)
				if array_find( stored_recipes, serialized ) == -1:
					target_block.get('craft').append( recipe )

	def remove( self, block_id : str ) -> dict | None:
		try: return self.recipes.pop( block_id )
		except: return None

	def update( self, values : dict ) -> None:
		for block_id, block_data in values.items():
			self.append(block_id, block_data)

	def clear( self ) -> None:
		self.recipes = dict()

	def serialize( self ) -> dict:
		return pickle.dumps( self.recipes )

	def deserialize( self, value : str ) -> None:
		self.recipes = pickle.loads( value )

	def resolve_tree( self, target_id : str, amount : int ) -> list[list[dict[str, int]]]:
		'''
		Resolve a list of lists which represent each depth of the crafting recipe and the materials in that level.

		Crafting Table IV but on drugs because flow diagrams can be created from each layer pointing to how the recipe is created in its full scale.
		'''
		raise NotImplementedError

	def resolve_multi_trees( self, targets : list[tuple[str, int]] ) -> dict[str, list[dict]]:
		'''
		Resolve multiple trees at once.
		'''
		raise NotImplementedError

	def resolve_materials( self, target_id : str, amount : int ) -> tuple[dict[str, int], int]:
		'''
		Resolve purely the bottom level materials only and return the amount of each raw material required to craft the item from the ground up.
		'''

		print(f'ROOT: {target_id}')
		root = self.recipes.get( target_id )

		assert root != None, 'Could not find the recipe as it does not exist!'
		assert array_find( root.get('sources'), ResourceType.CRAFTED ) != -1, 'The recipe is not a craftable item!'

		first_recipe = root.get('craft')[0].get('recipe')

		frontier = [
			(block_id, req_amount * amount)
			for block_id, req_amount in count_values( first_recipe ).items()
		]

		total_resources = { }
		total_smelts = 0

		while len(frontier) > 0:
			# print(frontier)
			# frontier = compress_frontier_array(frontier)
			# print(frontier)

			item = frontier.pop(0)
			item, total_items = item
			if item == None or item == 'minecraft:air':
				continue

			if item == target_id:
				raise ValueError('Recursive recipe detected! ' + str(target_id))

			recipe = self.recipes.get(item)
			# print(target_id, recipe)
			if recipe == None:
				print(f'Failed to find recipe for item {item}')
				continue

			# print(item)
			# print(recipe)

			source = recipe.get('sources')

			if array_find( source, ResourceType.SURFACE ) != -1 or array_find( source, ResourceType.UNDERGROUND ) != -1:

				# print('RESOURCE: ', recipe.get('blocks')[0], total_items )
				cache_increment_index( total_resources, recipe.get('blocks')[0], total_items )

			elif array_find( source, ResourceType.ORE_DROP ) != -1 or array_find( source, ResourceType.ORE ) != -1:

				cache_increment_index( total_resources, recipe.get('blocks')[0], total_items )

			elif array_find( source, ResourceType.CRAFTED ) != -1:

				# print( 'CRAFT: ', item, total_items )
				first_recipe = recipe.get('craft')[0]
				for block_id, amount_in_recipe in count_values(first_recipe.get('recipe')).items():
					second_recipe = self.recipes.get( block_id )
					if second_recipe == None:
						print('Failed to find sub-recipe of block id:', block_id)
						continue

					if array_find( second_recipe.get('sources'), ResourceType.CRAFTED ) == -1:
						frontier.append( (block_id, amount_in_recipe ) )
						continue
					second_out_per_craft = second_recipe.get('craft')[0].get('amount')
					p = ceil((total_items * amount_in_recipe) / second_out_per_craft)
					frontier.append( (block_id, p) )

			elif array_find( source, ResourceType.SMELTED ) != -1:
				# print('SMELT: ', item, total_items)
				smelted_block = recipe.get('smelt')[0]
				total_smelts += total_items
				frontier.append( (smelted_block, total_items) )
			else:
				raise ValueError(f'Unsupported Recipe Source: { [ resolve_source_id(idd) for idd in source ] }')

		# print('TOTAL_SMELTS: ', total_smelts)
		return total_resources, total_smelts


	def resolve_multi_materials( self, targets : list[tuple[str,int]], include_fuel : bool = True ) -> tuple[dict[str, int], int]:
		'''
		Resolve multiple bottom level materials for a list of blocks.
		'''
		total_resources : dict[str, int] = { }
		total_smelts : int = 0
		for (block_id, amount) in targets:
			resources, smelts = self.resolve_materials( block_id, amount )
			cache_push_increment( total_resources, resources )
			total_smelts += smelts
		if include_fuel == True:
			cache_increment_index(total_resources, 'minecraft:coal_ore', ceil(total_smelts / 8))
		return total_resources, total_smelts
