from .game_object import Component, GameObject, DEBUG
import pygame as pg
from .vmath_mini import Vector2d

from .transform import Transform

class SurfaceComponent(Component):
    pg_surf: pg.Surface
    size: Vector2d
    crop: bool

    def __init__(self, size: Vector2d, crop:bool=True):
        self.size = size
        self.pg_surf = pg.Surface(size.as_tuple(), pg.SRCALPHA, 32)
        self.crop = crop
        if DEBUG:
            self.pg_surf.set_alpha(128)

    def blit(self):
        if self.game_object == GameObject.root:
            return
        elif self.game_object.parent == GameObject.root:
            surf = self.game_object.parent.get_component(SurfaceComponent) 
            pos = self.game_object.get_component(Transform).pos - GameObject.get_group_by_tag("Camera")[0].get_component(Transform).pos
            pos += Vector2d.from_tuple(pg.display.get_surface().get_size())/2
        else:
            if self.crop:
                pos = self.game_object.get_component(Transform).pos + (self.game_object.parent.get_component(SurfaceComponent).size / 2)
                surf = self.game_object.parent.get_component(SurfaceComponent) 
            else:
                g_obj = self.game_object.parent
                surf = self.game_object.parent.get_component(SurfaceComponent) 
                abs_coords = self.game_object.get_component(Transform).pos
                def is_box_in_box(center_abs_pos: Vector2d, size1: Vector2d, size2: Vector2d) -> bool:
                    return (center_abs_pos - size1 / 2).is_in_box(size2 / -2, size2 / 2) and (center_abs_pos + size1 / 2).is_in_box(size2 / -2, size2 / 2)
                while g_obj != GameObject.root:
                    if is_box_in_box(abs_coords, self.size, g_obj.get_component(SurfaceComponent).size):
                        surf = g_obj.get_component(SurfaceComponent) 
                        break
                    abs_coords += g_obj.get_component(Transform).pos
                    g_obj = g_obj.parent
                pos = abs_coords + (g_obj.get_component(SurfaceComponent).size / 2)
        surf.pg_surf.blit(self.pg_surf, (pos - self.size / 2).as_tuple())


