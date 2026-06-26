from .game_object import Component
from .label import LabelComponent
import pygame as pg

class EntryComponent(LabelComponent):
    active: bool
    backspace_flag: bool
    backspace_timer: int

    backspace_cooldown: int = 10 # ticks

    def __init__(self, default_text: str = "", font = None, font_size: int = 32, active: bool = False):
        LabelComponent.__init__(self, default_text, font, font_size)
        self.active = active
        self.backspace_flag = False
        self.backspace_timer = 0
    
    def iteration(self):
        if self.active:
            need_update = False
            for event in pg.event.get(eventtype=pg.TEXTINPUT, pump=False):
                self.text += event.text
                need_update = True
            for event in pg.event.get(eventtype=pg.KEYDOWN, pump=False):
                if event.key == pg.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                        need_update = True
                        self.backspace_flag = True
            for event in pg.event.get(eventtype=pg.KEYUP, pump=False):
                if event.key == pg.K_BACKSPACE:
                    self.backspace_flag = False
                    self.backspace_timer = 0
            if self.backspace_flag:
                self.backspace_timer += 1
                if self.backspace_timer >= self.backspace_cooldown:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                        need_update = True
            if need_update:
                self.game_object.need_blit_set_true()
                self.game_object.need_draw = True

    def clear(self):
        self.text = ""
        self.game_object.need_draw = True
        self.game_object.need_blit_set_true()
    
    @staticmethod
    def refresh():
        pg.event.clear(eventtype=pg.TEXTINPUT)
        pg.event.clear(eventtype=pg.KEYDOWN)
        pg.event.clear(eventtype=pg.KEYUP)