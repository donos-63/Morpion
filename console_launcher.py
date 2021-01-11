from morbac import Morpion
from render.console_render import ConsoleRender

'''
Start Morpion with console interface
'''
render = ConsoleRender()
morbac = Morpion(render)
morbac.play()