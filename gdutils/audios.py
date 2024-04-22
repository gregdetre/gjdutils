import os
from playsound import playsound


def play_mp3(mp3_filen: str, prog: str = "pygame"):
    prog = prog.lower().strip()
    full_mp3_filen = os.path.abspath(os.path.expanduser(mp3_filen))
    if prog == "vlc":
        import vlc

        vlc_mp3_filen = os.path.join("file://", full_mp3_filen)
        p = vlc.MediaPlayer(vlc_mp3_filen)
        p.play()  # type: ignore
    elif prog == "pygame":
        import pygame

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(full_mp3_filen)
        pygame.mixer.music.play()
        pygame.event.wait()
    elif prog == "playsound":
        # https://stackoverflow.com/a/63147250/230523
        playsound(mp3_filen)
    elif prog == "cli":
        cmd = f"afplay -r 0.9 '{full_mp3_filen}'"
        # print(cmd)
        os.system(cmd)
    else:
        raise Exception(f"Unknown PROG '{prog}'")
    return full_mp3_filen
