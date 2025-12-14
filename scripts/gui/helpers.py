from PIL import Image, ImageEnhance
from pathlib import Path
from configparser import ConfigParser


PRINTER_DPI: int = 203


class ImageData:
    def __init__(self) -> None:
        self.img: Image.Image
        self.path: str
        self.origin_img: Image.Image


class QueuedProcess:
    def __init__(
        self, use_dither: bool, use_landscape: bool, brightness: float, dpi: float
    ) -> None:
        self.brightness: float = brightness
        self.use_landcape: bool = use_landscape
        self.use_dither: bool = use_dither
        self.dpi: float = dpi


def get_stem(path: str | None) -> str | None:
    if path:
        return Path(path).stem
    else:
        return None


def process_image(img: Image.Image, proc: QueuedProcess) -> Image.Image:
    proc_img: Image.Image = img
    # proc_img = proc_img.resize(convert_image_width(proc_img, proc.))

    brightn_enhance: ImageEnhance.Brightness = ImageEnhance.Brightness(img)
    proc_img = brightn_enhance.enhance(proc.brightness / 100)

    return proc_img


def parse_cfg_for_width() -> float:
    parser: ConfigParser = ConfigParser()
    width: float = 0.0
    try:
        parser.read("config.cfg")
    except Exception as error:
        raise error

    try:
        width = parser.getfloat("Settings", "PAPER_WIDTH")
    except Exception as error:
        raise error

    return width


def convert_image_width(
    image: Image.Image,
    paper_width: float,
    dpi: float,
    for_landscape_mode: bool = True,
) -> tuple[int, int]:
    width: int = image.width
    height: int = image.height
    aspect_ratio: float = width / height

    if for_landscape_mode:
        new_width: int = int(paper_width * dpi)
        new_height: int = int(new_width / aspect_ratio)
    else:
        new_height: int = int(paper_width * dpi)
        new_width: int = int(new_height / aspect_ratio)

    return (new_width, new_height)
