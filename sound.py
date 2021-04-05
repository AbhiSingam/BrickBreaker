import os


def play_shoot():
    os.system("aplay -q shoot_sound.wav &")

def play_bump():
    os.system("aplay -q bump.wav &")
