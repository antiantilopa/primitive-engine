from pathlib import Path
from typing import Callable
import pygame as pg
import numpy as np
import os, json
from .synths import LinearEnvelope, Synths, Note
from .game_object import Component
from .engine import Engine

class SoundComponent(Component):
    path: Path
    nickname: str
    volume: float
    tone_offset: float
    on_end: Callable
    is_music: bool
    sound: pg.mixer.Sound
    channels: list[pg.mixer.Channel]
    _event_type: int

    loaded_by_path: dict[Path, pg.mixer.Sound] = {}
    path_by_nickname: dict[str, Path] = {}
    instances: list["SoundComponent"] = []

    def __init__(self, path: str|Path = None, nickname: str = None, volume: float = 1, tone_offset: int = 0, on_end: Callable = lambda: None, is_music: bool = False):
        self.channels = []
        self.on_end = on_end
        self.is_music = is_music
        self._event_type = pg.event.custom_type()
        self.path = None
        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            assert isinstance(path, Path), "given path was not type 'str' nor 'pathlib.Path'"
        if path is None and nickname is None:
            raise ValueError("Either 'nickname' or 'path' must be provided.")
        elif nickname is None:
            SoundComponent.loaded_by_path[path] = SoundComponent.load(path)
            self.sound = SoundComponent.loaded_by_path[path]
        elif path is None:
            if nickname not in SoundComponent.path_by_nickname:
                raise ValueError(f"tried to load sound with nickname: '{nickname}' which is not registered")
            path = SoundComponent.path_by_nickname[nickname]
            if path not in SoundComponent.loaded_by_path:
                raise ValueError(f"tried to load sound with nickname: '{nickname}' which is associated with path: {path} that has not been loaded\n\n\tloaded paths: {SoundComponent.loaded_by_path}")
            self.sound = SoundComponent.loaded_by_path[path]
        else:
            print(f"creating sound with nickname: {nickname}")
            SoundComponent.path_by_nickname[nickname] = path
            SoundComponent.loaded_by_path[path] = SoundComponent.load(path)

        self.sound = SoundComponent.loaded_by_path[path]
        self.path = path
        self.nickname = nickname
        self.set_volume(volume)
        self.tone_offset = tone_offset
        SoundComponent.instances.append(self)

    def set_volume(self, volume: float = 1):
        self.volume = volume
        for channel in self.channels:
            channel.set_volume(volume)

    @staticmethod
    def load(path: Path|str) -> pg.mixer.Sound:
        if isinstance(path, str):
            path = Path(path)
        assert isinstance(path, Path), "given path was not type 'str' nor 'pathlib.Path'"
        assert os.path.exists(path / "config.json"), f"Sound config not found at path: {path}"
        config = json.load(open(path / "config.json"))
        parties = []
        Synths.seconds_per_note = config["spn"] if "spn" in config else 0.1
        for party_conf in config["parties"]:
            notes = Note.load_notes_new(path / party_conf["name"])
            tone_shift = 0
            envelope = LinearEnvelope(441, 441, 1.0, 1.0, 441) #default envelope
            if "tone_shift" in party_conf:
                tone_shift = party_conf["tone_shift"]
            if "envelope" in party_conf:
                envelope = LinearEnvelope(
                    attack = party_conf["envelope"].get("attack", 441),
                    decay = party_conf["envelope"].get("decay", 441),
                    sustain1 = party_conf["envelope"].get("sustain1", 1.0),
                    sustain2 = party_conf["envelope"].get("sustain2", 1.0),
                    release = party_conf["envelope"].get("release", 441)
                )
            
            party = Synths.get_party(notes, party_conf["wave"] if "wave" in party_conf else "sin", tone_shift, envelope)
            if "volume" in party_conf:
                party *= party_conf["volume"]
            if "roll" in party_conf:
                num = party_conf["roll"]["num"]
                delay = party_conf["roll"]["delay"]
                amplitudes = party_conf["roll"]["amplitudes"]
                party = Synths.reverb(party, num, delay, amplitudes)
            parties.append(party)
        arr = Synths.merge_parties(*parties)
        if "roll" in config:
            num = config["roll"]["num"]
            delay = config["roll"]["delay"]
            amplitudes = config["roll"]["amplitudes"]
            arr = Synths.reverb(arr, num, delay, amplitudes)
        sound = np.asarray([32767 * arr, 32767 * arr]).T.astype(np.int16)
        sound = pg.sndarray.make_sound(sound.copy())
        return sound

    @staticmethod
    def get_loaded_sound(nickname: str) -> pg.mixer.Sound:
        if nickname in SoundComponent.path_by_nickname:
            return SoundComponent.loaded_by_path[SoundComponent.path_by_nickname[nickname]]
        else:
            raise KeyError(f"Sound with nickname: '{nickname}' not found.")
    
    @staticmethod
    def is_downloaded(nickname: str = None, path: Path|str = None) -> bool:
        if nickname is None and path is None:
            raise ValueError("Either 'nickname' or 'path' must be provided.")
        if path is not None and nickname is not None:
            raise ValueError("Only one of 'nickname' or 'path' should be provided.")
        if path is not None:
            return path in SoundComponent.loaded_by_path
        if nickname is not None:
            return (nickname in SoundComponent.path_by_nickname) and (SoundComponent.path_by_nickname[nickname] in SoundComponent.loaded_by_path)
        
    def play_once(self) -> pg.mixer.Channel:
        channel = self.sound.play()
        if channel is None:
            return None
        channel.set_volume(self.volume)
        self.channels.append(channel)
        print(f"{self.nickname}: playing once thing with etype: {self._event_type}")
        channel.set_endevent(self._event_type)
        return channel

    def play_in_loop(self) -> pg.mixer.Channel:
        channel = self.sound.play(loops=-1)
        if channel is None:
            return None
        channel.set_volume(self.volume)
        self.channels.append(channel)
        channel.set_endevent(self._event_type)
        return channel
    
    def stop_channel(self, channel: pg.mixer.Channel):
        if channel in self.channels:
            channel.stop()
            self.channels.remove(channel)
    
    def stop_all_channels(self):
        for channel in self.channels:
            channel.stop()
        self.channels.clear()

    @staticmethod
    def refresh():
        for scomp in SoundComponent.instances:
            for event in pg.event.get(scomp._event_type, pump=False):
                i = 0
                while i < len(scomp.channels):
                    if scomp.channels[i].get_busy() == 0:
                        scomp.channels.pop(i)
                    else:
                        i += 1
                scomp.on_end()
                break


    def __del__(self):
        for channel in self.channels:
            channel.stop()
        self.channels.clear()
        if self in SoundComponent.instances:
            SoundComponent.instances.remove(self)
        if self.path in SoundComponent.loaded_by_path:
            SoundComponent.loaded_by_path.pop(self.path)
        self.sound = None
        del self.sound 
