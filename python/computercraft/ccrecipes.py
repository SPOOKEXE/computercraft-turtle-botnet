
import json

from minecraft.recipes import (
	RecipeHelpers, SmartRecipeSystem, ResourceType
)

DEFAULT_RECIPES = SmartRecipeSystem()

DEFAULT_RECIPES.update({
	"minecraft:cobblestone" :  RecipeHelpers.natural_resource(
		[ ResourceType.UNDERGROUND ],
		["minecraft:stone", "minecraft:cobblestone"]
	),

	"minecraft:stone" : RecipeHelpers.smeltable_resource([
		"minecraft:cobblestone"
	]),

	"minecraft:redstone_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:redstone_ore"]
	),

	"minecraft:deepslate_redstone_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:deepslate_redstone_ore"]
	),

	"minecraft:redstone" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE_DROP ],
		["minecraft:redstone_ore", "minecraft:deepslate_redstone_ore"]
	),

	"minecraft:coal_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:coal_ore"]
	),

	"minecraft:deepslate_coal_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:deepslate_coal_ore"]
	),

	"minecraft:coal" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE_DROP ],
		["minecraft:coal_ore", "minecraft:deepslate_coal_ore"]
	),

	"minecraft:coal_block" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
			"minecraft:coal", "minecraft:coal", "minecraft:coal",
		),
	]),

	"minecraft:iron_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:iron_ore"]
	),

	"minecraft:deepslate_iron_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		["minecraft:deepslate_iron_ore"]
	),

	"minecraft:raw_iron" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE_DROP ],
		["minecraft:iron_ore", "minecraft:deepslate_iron_ore"]
	),

	'minecraft:iron_ingot' : RecipeHelpers.smeltable_resource([
		"minecraft:raw_iron"
	]),

	"minecraft:sand" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:sand" ]
	),

	"minecraft:glass" : RecipeHelpers.smeltable_resource([
		"minecraft:sand"
	]),

	"minecraft:glass_pane" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			16,
			"minecraft:glass", "minecraft:glass", "minecraft:glass",
			"minecraft:glass", "minecraft:glass", "minecraft:glass",
		),
	]),

	"minecraft:oak_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:oak_log" ]
	),

	"minecraft:oak_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:oak_log" )
	]),

	"minecraft:spruce_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:spruce_log" ]
	),

	"minecraft:spruce_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:spruce_log" )
	]),

	"minecraft:birch_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:birch_log" ]
	),

	"minecraft:birch_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:birch_log" )
	]),

	"minecraft:jungle_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:jungle_log" ]
	),

	"minecraft:jungle_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:jungle_log" )
	]),

	"minecraft:acacia_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:acacia_log" ]
	),

	"minecraft:acacia_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:acacia_log" )
	]),

	"minecraft:dark_oak_log" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:dark_oak_log" ]
	),

	"minecraft:dark_oak_planks" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe( 4, "minecraft:dark_oak_log" )
	]),

	"minecraft:stick" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:oak_planks", None, None,
			"minecraft:oak_planks", None, None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:spruce_planks", None, None,
			"minecraft:spruce_planks", None, None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:birch_planks", None, None,
			"minecraft:birch_planks", None, None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:jungle_planks", None, None,
			"minecraft:jungle_planks", None, None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:dark_oak_planks", None, None,
			"minecraft:dark_oak_planks", None, None,
		),
	]),

	"minecraft:crafting_table" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:oak_planks", "minecraft:oak_planks", None,
			"minecraft:oak_planks", "minecraft:oak_planks", None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:spruce_planks", "minecraft:spruce_planks", None,
			"minecraft:spruce_planks", "minecraft:spruce_planks", None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:birch_planks", "minecraft:birch_planks", None,
			"minecraft:birch_planks", "minecraft:birch_planks", None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:jungle_planks", "minecraft:jungle_planks", None,
			"minecraft:jungle_planks", "minecraft:jungle_planks", None,
		),
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", None,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", None,
		),
	]),

	"minecraft:iron_pickaxe" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot",
			None, "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:iron_shovel" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			4,
			None, "minecraft:iron_ingot", None,
			None, "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:iron_axe" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			4,
			"minecraft:iron_ingot", "minecraft:iron_ingot", None,
			"minecraft:iron_ingot", "minecraft:stick", None,
			None, "minecraft:stick", None,
		)
	]),

	"minecraft:chest" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:oak_planks", "minecraft:oak_planks", "minecraft:oak_planks",
			"minecraft:oak_planks", None, "minecraft:oak_planks",
			"minecraft:oak_planks", "minecraft:oak_planks", "minecraft:oak_planks",
		),
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:spruce_planks", "minecraft:spruce_planks", "minecraft:spruce_planks",
			"minecraft:spruce_planks", None, "minecraft:spruce_planks",
			"minecraft:spruce_planks", "minecraft:spruce_planks", "minecraft:spruce_planks",
		),
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:birch_planks", "minecraft:birch_planks", "minecraft:birch_planks",
			"minecraft:birch_planks", None, "minecraft:birch_planks",
			"minecraft:birch_planks", "minecraft:birch_planks", "minecraft:birch_planks",
		),
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:jungle_planks", "minecraft:jungle_planks", "minecraft:jungle_planks",
			"minecraft:jungle_planks", None, "minecraft:jungle_planks",
			"minecraft:jungle_planks", "minecraft:jungle_planks", "minecraft:jungle_planks",
		),
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:acacia_planks", "minecraft:acacia_planks", "minecraft:acacia_planks",
			"minecraft:acacia_planks", None, "minecraft:acacia_planks",
			"minecraft:acacia_planks", "minecraft:acacia_planks", "minecraft:acacia_planks",
		),
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks",
			"minecraft:dark_oak_planks", None, "minecraft:dark_oak_planks",
			"minecraft:dark_oak_planks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks",
		),
	]),

	"computercraft:computer_normal" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:stone", "minecraft:stone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
			"minecraft:stone", "minecraft:glass_pane", "minecraft:stone",
		),
	]),

	"computercraft:turtle_normal" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:iron_ingot", "minecraft:iron_ingot", "minecraft:iron_ingot",
			"minecraft:iron_ingot", "computercraft:computer_normal", "minecraft:iron_ingot",
			"minecraft:iron_ingot", "minecraft:chest", "minecraft:iron_ingot",
		),
	]),

	"minecraft:sugar_cane" :  RecipeHelpers.natural_resource(
		[ ResourceType.SURFACE ],
		[ "minecraft:sugar_cane" ]
	),

	"minecraft:lapis_lazuli" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE_DROP ],
		[ "minecraft:lapis_ore", "minecraft:deepslate_lapis_ore" ]
	),

	"minecraft:lapis_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		[ "minecraft:lapis_ore" ]
	),

	"minecraft:deepslate_lapis_ore" :  RecipeHelpers.natural_resource(
		[ ResourceType.ORE ],
		[ "minecraft:deepslate_lapis_ore" ]
	),

	"minecraft:paper" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			3,
			"minecraft:sugar_cane", "minecraft:sugar_cane", "minecraft:sugar_cane"
		),
	]),

	"minecraft:blue_dye" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:lapis_lazuli"
		),
	]),

	"minecraft:furnace" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:cobblestone", "minecraft:cobblestone", "minecraft:cobblestone",
			"minecraft:cobblestone", None, "minecraft:cobblestone",
			"minecraft:cobblestone", "minecraft:cobblestone", "minecraft:cobblestone",
		),
	]),

	"computercraft:disk" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:redstone", "minecraft:paper", None,
			"minecraft:blue_dye", None, None,
		),
	]),

	"computercraft:disk_drive" : RecipeHelpers.craftable_resource([
		RecipeHelpers.construct_craft_recipe(
			1,
			"minecraft:stone", "minecraft:stone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
			"minecraft:stone", "minecraft:redstone", "minecraft:stone",
		),
	]),
})

# if __name__ == '__main__':

# 	# print( json.dumps(DEFAULT_RECIPES.recipes, indent=4) )
# 	# with open('output.txt', 'wb') as file:
# 	# 	file.write(DEFAULT_RECIPES.serialize())

# 	print('MATERIALS 1')
# 	recipe_depths = DEFAULT_RECIPES.resolve_materials( 'computercraft:turtle_normal', 1 )
# 	print( json.dumps(recipe_depths, indent=4) )

# 	print('MATERIALS 2')
# 	total_resources, total_smelts = DEFAULT_RECIPES.resolve_multi_materials([
# 		('computercraft:turtle_normal', 1),
# 		('minecraft:iron_pickaxe', 1),
# 		('minecraft:iron_shovel', 1),
# 		('minecraft:iron_axe', 1),
# 		('minecraft:crafting_table', 1),
# 		('minecraft:furnace', 3),
# 		('computercraft:disk', 1),
# 		('computercraft:disk_drive', 1),
# 		('minecraft:coal_block', 1),
# 	])
# 	print( json.dumps(total_resources, indent=4), total_smelts )
