from pygame import mixer 

mixer.init()

class Sound: 
    def __init__(self, path):
        self.sound = mixer.Sound(path)
    def play(self):
        mixer.Sound.play(self.sound)

def init_music(path, volume):
    mixer.music.load(path)
    mixer.music.play(-1)
    mixer.music.set_volume(volume)