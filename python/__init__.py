
from computercraft import CCWorld
from turtle_botnet import TurtleWebsocket

# from turtle_bt import (

# )

# TODO: save and load world
# TODO: start behavior trees

world = CCWorld()

ccwebsocket = TurtleWebsocket( world )
ccwebsocket.start()
