
from __future__ import annotations

import json

from enum import Enum
from math import ceil
from typing import Any

from utility import array_find, cache_increment_index, cache_push_increment

class RecipeType(Enum):
	SURFACE = 0
	UNDERGROUND = 1

	ORE = 5
	ORE_DROP = 6

	CRAFT = 8
	SMELT = 9

def construct_craft_recipe( amount : int, *args : str ) -> list[str]:
	recipe = [None] * 9
	for index, value in enumerate(args): recipe[index] = value
	return { 'recipe' : recipe, 'amount' : amount}

def natural_resource( sources : list, blocks : list ) -> dict:
	return { 'sources' : sources, 'blocks' : blocks, 'craft' : None, 'smelt' : None }

def craftable_resource( recipes : list[list] ) -> dict:
	return { 'sources' : [ RecipeType.CRAFT ], 'blocks' : None, 'craft' : recipes, 'smelt' : None }

def smeltable_resource( blocks : list[str] ) -> dict:
	return { 'sources' : [ RecipeType.SMELT ], 'blocks' : None, 'craft' : None, 'smelt' : blocks }

RECIPES = {

	"minecraft:cobblestone" : natural_resource(
		[ RecipeType.UNDERGROUND ],
		["minecraft:cobblestone"]
	),

	"minecraft:stone" : smeltable_resource([
		"minecraft:cobblestone"
	]),

	"minecraft:redstone_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:redstone_ore"]
	),

	"minecraft:deepslate_redstone_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:deepslate_redstone_ore"]
	),

	"minecraft:redstone" : natural_resource(
		[ RecipeType.ORE_DROP ],
		["minecraft:redstone_ore", "minecraft:deepslate_redstone_ore"]
	),

	"minecraft:coal_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:coal_ore"]
	),

	"minecraft:deepslate_coal_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:deepslate_coal_ore"]
	),

	"minecraft:coal" : natural_resource(
		[ RecipeType.ORE_DROP ],
		["minecraft:coal_ore", "minecraft:deepslate_coal_ore"]
	),

	"minecraft:coal_block" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
		),
	]),

	"minecraft:iron_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:iron_ore"]
	),

	"minecraft:deepslate_iron_ore" : natural_resource(
		[ RecipeType.ORE ],
		["minecraft:deepslate_iron_ore"]
	),

	"minecraft:raw_iron" : natural_resource(
		[ RecipeType.ORE_DROP ],
		["minecraft:iron_ore", "minecraft:deepslate_iron_ore"]
	),

	'minecraft:iron_ingot' : smeltable_resource([
		"minecraft:raw_iron"
	]),

	"minecraft:sand" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:sand" ]
	),

	"minecraft:glass" : smeltable_resource([
		"minecraft:sand"
	]),

	"minecraft:glass_pane" : craftable_resource([
		construct_craft_recipe(
			16,
			"minecraft:glass", "minecraft:glass", "minecraft:glass",
			"minecraft:glass", "minecraft:glass", "minecraft:glass",
		),
	]),

	"minecraft:oak_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:oak_log" ]
	),

	"minecraft:oak_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:oak_log" )
	]),

	"minecraft:spruce_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:spruce_log" ]
	),

	"minecraft:spruce_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:spruce_log" )
	]),

	"minecraft:birch_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:birch_log" ]
	),

	"minecraft:birch_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:birch_log" )
	]),

	"minecraft:jungle_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:jungle_log" ]
	),

	"minecraft:jungle_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:jungle_log" )
	]),

	"minecraft:acacia_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:acacia_log" ]
	),

	"minecraft:acacia_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:acacia_log" )
	]),

	"minecraft:dark_oak_log" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:dark_oak_log" ]
	),

	"minecraft:dark_oak_planks" : craftable_resource([
		construct_craft_recipe( 4, "minecraft:dark_oak_log" )
	]),

	"minecraft:stick" : craftable_resource([
		construct_craft_recipe(
			4,
			"minecraft:oak_planks", None, None,
			"minecraft:oak_planks", None, None,
		),
		construct_craft_recipe(
			4,
			"minecraft:spruce_planks", None, None,
			"minecraft:spruce_planks", None, None,
		),
		construct_craft_recipe(
			4,
			"minecraft:birch_planks", None, None,
			"minecraft:birch_planks", None, None,
		),
		construct_craft_recipe(
			4,
			"minecraft:jungle_planks", None, None,
			"minecraft:jungle_planks", None, None,
		),
		construct_craft_recipe(
			4,
			"minecraft:dark_oak_planks", None, None,
			"minecraft:dark_oak_planks", None, None,
		),
	]),

	"minecraft:crafting_table" : craftable_resource([
		construct_craft_recipe(
			4,
			"minecraft:oak_planks", "minecraft:oak_planks", None,
			"minecraft:oak_planks", "minecraft:oak_planks", None,
		),
		construct_craft_recipe(
			4,
			"minecraft:spruce_planks", "minecraft:spruce_planks", None,
			"minecraft:spruce_planks", "minecraft:spruce_planks", None,
		),
		construct_craft_recipe(
			4,
			"minecraft:birch_planks", "minecraft:birch_planks", None,
			"minecraft:birch_planks", "minecraft:birch_planks", None,
		),
		construct_craft_recipe(
			4,
			"minecraft:jungle_planks", "minecraft:jungle_planks", None,
			"minecraft:jungle_planks", "minecraft:jungle_planks", None,
		),
		construct_craft_recipe(
			4,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", None,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", None,
		),
	]),

	"minecraft:iron_pickaxe" : craftable_resource([
		construct_craft_recipe(
			4,
			"minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot",
			None, "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:iron_shovel" : craftable_resource([
		construct_craft_recipe(
			4,
			None, "minecraft:iron_ingot", None,
			None, "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:iron_axe" : craftable_resource([
		construct_craft_recipe(
			4,
			"minecraft:iron_ingot", "minecraft:iron_ingot", None,
			"minecraft:iron_ingot", "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:chest" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:oak_planks", "minecraft:oak_planks", "minecraft:oak_planks",
			"minecraft:oak_planks", None, "minecraft:oak_planks",
			"minecraft:oak_planks", "minecraft:oak_planks", "minecraft:oak_planks",
		),
		construct_craft_recipe(
			1,
			"minecraft:spruce_planks", "minecraft:spruce_planks", "minecraft:spruce_planks",
			"minecraft:spruce_planks", None, "minecraft:spruce_planks",
			"minecraft:spruce_planks", "minecraft:spruce_planks", "minecraft:spruce_planks",
		),
		construct_craft_recipe(
			1,
			"minecraft:birch_planks", "minecraft:birch_planks", "minecraft:birch_planks",
			"minecraft:birch_planks", None, "minecraft:birch_planks",
			"minecraft:birch_planks", "minecraft:birch_planks", "minecraft:birch_planks",
		),
		construct_craft_recipe(
			1,
			"minecraft:jungle_planks", "minecraft:jungle_planks", "minecraft:jungle_planks",
			"minecraft:jungle_planks", None, "minecraft:jungle_planks",
			"minecraft:jungle_planks", "minecraft:jungle_planks", "minecraft:jungle_planks",
		),
		construct_craft_recipe(
			1,
			"minecraft:acacia_planks", "minecraft:acacia_planks", "minecraft:acacia_planks",
			"minecraft:acacia_planks", None, "minecraft:acacia_planks",
			"minecraft:acacia_planks", "minecraft:acacia_planks", "minecraft:acacia_planks",
		),
		construct_craft_recipe(
			1,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks",
			"minecraft:dark_oak_planks", None, "minecraft:dark_oak_planks",
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks",
		),
	]),

	"computercraft:computer_normal" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:stone", "minecraft:stone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
			"minecraft:stone", "minecraft:glass_pane", "minecraft:stone",
		),
	]),

	"computercraft:turtle_normal" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot",
			"minecraft:iron_ingot", "computercraft:computer_normal", "minecraft:iron_ingot",
			"minecraft:iron_ingot", "minecraft:chest", "minecraft:iron_ingot",
		),
	]),

	"minecraft:sugar_cane" : natural_resource(
		[ RecipeType.SURFACE ],
		[ "minecraft:sugar_cane" ]
	),

	"minecraft:lapis_lazuli" : natural_resource(
		[ RecipeType.ORE_DROP ],
		[ "minecraft:lapis_ore", "minecraft:deepslate_lapis_ore" ]
	),

	"minecraft:lapis_ore" : natural_resource(
		[ RecipeType.ORE ],
		[ "minecraft:lapis_ore" ]
	),

	"minecraft:deepslate_lapis_ore" : natural_resource(
		[ RecipeType.ORE ],
		[ "minecraft:deepslate_lapis_ore" ]
	),

	"minecraft:paper" : craftable_resource([
		construct_craft_recipe(
			3,
			"minecraft:sugar_cane", "minecraft:sugar_cane", "minecraft:sugar_cane"
		),
	]),

	"minecraft:blue_dye" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:lapis_lazuli"
		),
	]),

	"minecraft:furnace" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:cobblestone", "minecraft:cobblestone", "minecraft:cobblestone",
			"minecraft:cobblestone", None, "minecraft:cobblestone",
			"minecraft:cobblestone", "minecraft:cobblestone", "minecraft:cobblestone",
		),
	]),

	"computercraft:disk" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:redstone", "minecraft:paper", None,
			"minecraft:blue_dye", None, None,
		),
	]),

	"computercraft:disk_drive" : craftable_resource([
		construct_craft_recipe(
			1,
			"minecraft:stone", "minecraft:stone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
		),
	]),

}

def count_values( array : list ) -> dict:
	values = { }
	for value in array:
		if value != None and value != 'minecraft:air':
			cache_increment_index( values, value, 1 )
	return values

def resolve_source_id( target : int ) -> str:
	for (name, value) in RecipeType.__dict__.items():
		if name.find('__') == -1 and value == target:
			return name
	return "unknown"

def resolve_recipe_tree( target_id : str, total_amount : int ) -> tuple[dict, int]:
	root_item = RECIPES.get(target_id)
	# print(f'ROOT: {target_id}')

	assert root_item != None, 'Could not find the recipe because it does not exist!'
	assert array_find( root_item.get('sources'), RecipeType.CRAFT ) != -1, 'The recipe is not a craftable item!'

	first_recipe = root_item.get('craft')[0].get('recipe')

	# resolve the first frontier
	frontier = [
		(block_id, req_amount * total_amount)
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

		recipe = RECIPES.get(item)
		# print(target_id, recipe)
		if recipe == None:
			print(f'Failed to find recipe for item {item}')
			continue

		# print(item)
		# print(recipe)

		source = recipe.get('sources')

		if array_find( source, RecipeType.SURFACE ) != -1 or array_find( source, RecipeType.UNDERGROUND ) != -1:

			# print('RESOURCE: ', recipe.get('blocks')[0], total_items )
			cache_increment_index( total_resources, recipe.get('blocks')[0], total_items )

		elif array_find( source, RecipeType.ORE_DROP ) != -1 or array_find( source, RecipeType.ORE ) != -1:

			cache_increment_index( total_resources, recipe.get('blocks')[0], total_items )

		elif array_find( source, RecipeType.CRAFT ) != -1:

			# print( 'CRAFT: ', item, total_items )

			first_recipe = recipe.get('craft')[0]
			# first_out_per_craft = first_recipe.get('amount')
			# print( 'count recipe: ', item, first_out_per_craft )

			for block_id, amount_in_recipe in count_values(first_recipe.get('recipe')).items():

				second_recipe = RECIPES.get( block_id )
				if second_recipe == None:
					print('Failed to find sub-recipe of block id:', block_id)
					continue

				if array_find( second_recipe.get('sources'), RecipeType.CRAFT ) == -1:
					frontier.append( (block_id, amount_in_recipe ) )
					continue

				second_out_per_craft = second_recipe.get('craft')[0].get('amount')
				# print( block_id, second_out_per_craft )

				p = ceil((total_items * amount_in_recipe) / second_out_per_craft)
				# print( p )

				frontier.append( (block_id, p) )

		elif array_find( source, RecipeType.SMELT ) != -1:
			# print('SMELT: ', item, total_items)
			smelted_block = recipe.get('smelt')[0]
			total_smelts += total_items
			frontier.append( (smelted_block, total_items) )
		else:
			raise ValueError(f'Unsupported Recipe Source: { [ resolve_source_id(idd) for idd in source ] }')

	# print('TOTAL_SMELTS: ', total_smelts)
	return total_resources, total_smelts

def resolve_multi_tree( items : list[tuple[str, int]], include_fuel : bool = True ) -> tuple[dict, int]:
	print('-- Resolve Multi-Recipe Material Requirements --')
	total_resources = { }
	total_smelts = 0
	for (item_id, amount) in items:
		print(item_id, amount)
		resources, smelts = resolve_recipe_tree( item_id, amount )
		# print(item_id, resources)
		# print(resources, smelts)
		cache_push_increment( total_resources, resources )
		total_smelts += smelts
	if include_fuel == True:
		cache_increment_index(total_resources, 'minecraft:coal_ore', ceil(total_smelts / 8))
	return total_resources, total_smelts

if __name__ == '__main__':

	total_resources, total_smelts = resolve_multi_tree([
		('computercraft:turtle_normal', 1),
		('minecraft:iron_pickaxe', 1),
		('minecraft:iron_shovel', 1),
		('minecraft:iron_axe', 1),
		('minecraft:crafting_table', 1),
		('minecraft:furnace', 3),
		('computercraft:disk', 1),
		('computercraft:disk_drive', 1),
		('minecraft:coal_block', 1),
	])

	print( json.dumps(total_resources, indent=4) )
