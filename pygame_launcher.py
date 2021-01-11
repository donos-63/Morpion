from morbac import Morpion
from render.pygame_render import PygameRender


render = PygameRender()
morbac = Morpion(render)
morbac.play()