import os
from typing import Optional


def play_mp3(mp3_filen: str, prog: str = "cli", speed: Optional[float] = None):
    prog = prog.lower().strip()
    full_mp3_filen = os.path.abspath(os.path.expanduser(mp3_filen))
    if prog == "vlc":
        # pip install python-vlc
        import vlc

        vlc_mp3_filen = os.path.join("file://", full_mp3_filen)
        p = vlc.MediaPlayer(vlc_mp3_filen)
        if speed is not None:
            p.set_rate(speed)  # type: ignore
        p.play()  # type: ignore
    elif prog == "pygame":
        assert speed is None, "Not implemented speed for pygame"
        import pygame

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(full_mp3_filen)
        pygame.mixer.music.play()
        pygame.event.wait()
    elif prog == "playsound":
        # maybe set to 1.2.2 if you're having trouble installing
        from playsound import playsound

        assert speed is None, "Playsound doesn't support changing speed"
        # https://stackoverflow.com/a/63147250/230523
        playsound(mp3_filen)
    elif prog == "cli":
        cmd = f"afplay -r {speed} '{full_mp3_filen}'"
        # print(cmd)
        os.system(cmd)
    else:
        raise Exception(f"Unknown PROG '{prog}'")
    return full_mp3_filen
