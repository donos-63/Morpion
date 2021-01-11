from morbac import Morpion
from render.console_render import ConsoleRender

render = ConsoleRender()
morbac = Morpion(render)
morbac.play()