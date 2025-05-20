import pygame


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music = None
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self._load_assets()

    def set_mute(self, mute: bool):
        self.music_volume = 0.0 if mute else 0.5
        self.sound_volume = 0.0 if mute else 0.7
        if self.music:
            self.music.set_volume(self.music_volume)

    def _load_assets(self):
        try:
            self.music = pygame.mixer.Sound('assets/sounds/background.mp3')
            self.sounds = {
                'select': pygame.mixer.Sound('assets/sounds/select.mp3'),
                'swap_success': pygame.mixer.Sound('assets/sounds/swap_success.mp3'),
                'swap_fail': pygame.mixer.Sound('assets/sounds/swap_fail.mp3'),
                'match': pygame.mixer.Sound('assets/sounds/match.mp3')
            }
        except Exception as e:
            print(f"Could not load audio: {e}")
            self.music = None
            self.sounds = {
                'select': None,
                'swap_success': None,
                'swap_fail': None,
                'match': None
            }

    def play_music(self, loop=True):
        if self.music:
            self.music.set_volume(self.music_volume)
            self.music.play(-1 if loop else 0)

    def stop_music(self):
        if self.music:
            self.music.stop()

    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].set_volume(self.sound_volume)
            self.sounds[sound_name].play()
