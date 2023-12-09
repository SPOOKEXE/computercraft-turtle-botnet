
## ComputerCraft Turtle BotNet

ComputerCraft Turtles that self-replicate by mining their own resources and crafting the necessary components for new turtles to be created.

After several turtles have been created, it starts another system which acts as a complex 'hive' mind that has leader-driven behavior.
This will give turtles specific jobs, such as farming trees, mining resources, crafting materials, smelting resources, etc.

## How It Works

For this implementation of the system, I have **python** handle the majority of the calculations, behaviors and procedures of the turtles

For the turtles, I make them simply connect to python with webhooks to find out what they need to do next, and I keep state persistence inside the turtles for when they are chunk unloaded and reloaded as it resets the turtle's VM.

The following high-level diagram shows this complete turtle-perspective process.

<img src="docs/readme/high-level-turtle-flow.png" alt="Turtle-Perspective Flowchart" width="300px"></img>

For the python backend, there is many pieces to the puzzle, so here is quick list of components:
1. **CORE COMPONENTS:**
	a. Websocket Wrapper
	b. Behavior Tree System
	c. Recipe Resolver
	d. Asynchronous Operations

2. **EXTRA COMPONENTS:**
	a. 3D World Visualizer
	b. Fully Serializable

And here is a version of the turtle behavior tree diagram:
<img src="docs/readme/turtle-brain-diagram.png" alt="Behavior Trees Flowchart" width="800px"></img>

...
...
...

## Installation

#### Python
1. Have any version of `python 3` installed.
2. Run `pip install -r requirements.txt`

#### ComputerCraft
1. Install `ComputerCraft` or `ComputerCraft:Tweaked`; any version is supported that has `websockets`.

## How To Use

#### Python

0. View the installation section if you have not yet.
1. Run the following script; `python -> __init__.py`

#### ComputerCraft
1. In your `Minecraft World Folder`, allow websocket connections to your host in the `World Folder -> serverconfig -> computercraft-server.toml` file.

2. Pick one of the following options depending on what is your circumstance:

	**Singleplayer (World Folder):**
	i. Copy `turtle -> main -> startup.lua` from this repository to your `turtle folder`.
	You can find the turtle folder in the `minecraft world folder -> computercraft -> computer -> [TURTLE_ID]` folder. If you need to find your turtle id, open the target turtle and run `id`.
	ii. Reboot the turtle.

	**SinglePlayer & Multiplayer (Pastebin):**
	i. Upload `turtle -> main -> startup.lua` to pastebin.
	ii. In the target turtle, use `pastebin [URL_HERE] startup.lua`, replacing `[URL_HERE]` with the pastebin url.
	iii. Reboot the turtle.

	**Singleplayer & Multiplayer (Manual):**
	i. Open the `turtle -> main -> startup.lua` file in this repository.
	ii. In the target turtle, type `edit startup.lua`.
	iii. Copy each line from the `startup.lua` individually into the computercraft editor.
	iv. Press `CTRL / COMMAND` and `SAVE` using the arrow keys and enter.
	v. Press `CTRL / COMMAND` and `EXIT` using the arrow keys and enter.
	vi. Reboot the turtle.

## Resources / Credits

`99%` of the code was done by me, [@SPOOKEXE](https://www.github.com/SPOOKEXE).

I used a resource to solve the turtle replication which is linked below; namely the `genesis` function.
<img src="docs/readme/credits-resource-1.png" alt="YouTube Video Thumbnail" width="600px"></img>
**Video:** https://www.youtube.com/watch?v=MXYZufNQtdQ
**Code:** https://pastebin.com/YtvRxY9j

Another video resource I used as a 'goal' for the project was to visualize what the turtles see in a 3D space:
<img src="docs/readme/credits-resource-1.png" alt="YouTube Video Thumbnail" width="600px"></img>
**Video:** https://www.youtube.com/watch?v=pwKRbsDbxqc

Finally, the last video reference I used was for general application to any turtle program; to get an idea of state persistence.
<img src="docs/readme/credits-resource-3.png" alt="YouTube Video Thumbnail" width="600px"></img>
**Video:** https://www.youtube.com/watch?v=U7HWMfgPGxo

Apart from those, I did everything from the ground up.
