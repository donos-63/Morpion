from morbac import Morpion
from render.pygame_render import PygameRender

'''
Start Morpion with graphical interface
'''
render = PygameRender()
morbac = Morpion(render)
morbac.play()