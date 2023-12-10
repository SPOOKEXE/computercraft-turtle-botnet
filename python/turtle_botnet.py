
from computercraft import (
	# library
	BaseBehaviorTree, BehaviorTreeBuilder,
	BaseSequenceItem, TreeNodeFactory,
	# websocket
	BaseWebSocket,
	# ccminecraft
	CCWorldAPI,
	# consts
	CCTurtle, CCWorld, TurtleActions
)

from minecraft import (
	# consts.py
	Direction, Point3, Item,
	Inventory, Block, SolidBlock,
	Chest, Furnace,
	# world.py
	WorldAPI,
	# recipes.py
	RecipeType, SmartRecipeSystem,
	resolve_recipe_tree, resolve_multi_tree,
	craftable_resource, natural_resource, smeltable_resource,
)

minecraft_recipes = SmartRecipeSystem()
minecraft_recipes.set_json({
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
})
