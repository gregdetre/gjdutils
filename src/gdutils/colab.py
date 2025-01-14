import os

from .runtime import in_colab

# https://stackoverflow.com/a/53586419/230523
IN_COLAB = in_colab()
# also specified in authortools_demo.ipynb
GOOGLE_DRIVE_MOUNT_PATH = "/content/drive"
GOOGLE_DRIVE_OUTPUT_PATH = os.path.join(
    GOOGLE_DRIVE_MOUNT_PATH,
    "Shareddrives",
    "Blah",  # TODO
)


def colab_path_if_needed(filen: str):
    """
    Prepend the Google Drive mount path for Colab if IN_COLAB is True.
    """
    if IN_COLAB:
        filen = os.path.join(GOOGLE_DRIVE_OUTPUT_PATH, filen)
    return filen


def set_css_for_colab():
    from IPython.display import HTML, display

    # from https://stackoverflow.com/a/61401455/230523
    display(
        HTML(
            """
        <style>
            pre { 
                white-space: pre-wrap;
            }
        </style>
        """
        )
    )
