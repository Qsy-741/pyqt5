import os
import winsound
from Basedir import basedir


def play_sound(filename):
    filepath = os.path.join(basedir, 'resource', filename)
    winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)


# name = "叮咚叮咚.wav"
# play_sound(name)
# while True:
#     pass
