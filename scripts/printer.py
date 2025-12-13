import sys
import configparser as cfgp
from PIL import Image
from colorama import Fore
from os import mkdir
from os.path import join, exists
from pathlib import Path


class ImageData:
    def __init__(self, img: Image.Image, path: str) -> None:
        self.img = img
        self.path = path


PRINTER_DPI: int = 203


def get_image_path() -> str:
    path: str = ""
    if len(sys.argv) > 1:
        try:
            path = sys.argv[1]
        except Exception as error:
            print(f"{Fore.RED}Argument incorrect.\nErreur: {error}{Fore.RESET}")

    while not path:
        path = input(f"{Fore.YELLOW}Chemin de l'image à convertir:{Fore.RESET} ")
    else:
        print(f"{Fore.GREEN}Fichier:{Fore.RESET} {path}")

    return path


def open_image(path: str) -> Image.Image | None:
    img: Image.Image
    try:
        img = Image.open(path)
    except Exception as error:
        print(f"{Fore.RED}Chemin de l'image incorrect.\nError: {error}{Fore.RESET}")
        return

    return img


def get_paper_width() -> float:
    cfg_parser: cfgp.ConfigParser = cfgp.ConfigParser()
    paper_width: float = parse_cfg_for_width(cfg_parser)
    while not paper_width:
        try:
            paper_width = float(
                input(
                    f"{Fore.YELLOW}Largeur en pouces du papier d'imprimante:{Fore.RESET} "
                )
            )
        except Exception as error:
            print(f"{Fore.RED}Taille du papier incorrecte.\nError: {error}{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}Taille papier reconnue: {paper_width}{Fore.GREEN}")

    return paper_width


def img_convert_rgb(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA"):
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        white_bg.paste(img, mask=img.split()[-1])
        img = white_bg
    return img.convert("RGB")


def is_landscape_select() -> bool:
    landscape_select: str = ""
    landscape_message: str = (
        f"{Fore.YELLOW}Préparer une image pour une impression P[O]RTRAIT ou P[A]YSAGE ?  O/A: "
    )
    while landscape_select != "o" and landscape_select != "a":
        landscape_select = input(landscape_message).lower()

    return True if landscape_select == "a" else False


def ask_brightness_level() -> float:
    brightness: float = 0.0
    while not brightness:
        try:
            brightness = float(input(f"{Fore.YELLOW}% de luminosité:{Fore.RESET} "))
        except Exception as error:
            print(f"{Fore.RED}Luminosité incorrecte.\nError: {error}{Fore.RESET}")
    return brightness


def dither(img: Image.Image) -> Image.Image:
    is_dithering_str: str = ""
    while is_dithering_str != "y" and is_dithering_str != "n":
        is_dithering_str = input(
            f"{Fore.YELLOW}Appliquer dither ? Y/N:{Fore.RESET} "
        ).lower()
    if is_dithering_str == "y":
        return img.convert(mode="1", dither=Image.Dither.FLOYDSTEINBERG)
    else:
        return img.convert(mode="1", dither=Image.Dither.NONE)


def save_image(img: Image.Image, path: str, save_suffix: int) -> None:
    base_name: str = Path(path).stem
    output_name: str = f"{base_name}_{save_suffix}.png"
    output_dir: str = "output"
    output_full: str = join(output_dir, output_name)

    if not exists(output_dir):
        mkdir(output_dir)

    img.show(output_name)
    img.save(output_full)
    print(f"{Fore.GREEN}Image sauvergardé -> {output_name}{Fore.RESET}")


def ask_quit() -> bool:
    reset_str: str = ""
    while reset_str != "y" and reset_str != "n":
        reset_str = input(f"{Fore.YELLOW}Recommencer ? Y/N:{Fore.RESET} ").lower()
    return True if reset_str == "y" else False


def change_luminosity(
    image: Image.Image,
    luminosity: float,
) -> Image.Image:
    luminosity = luminosity / 100.0
    width: int = image.size[0]
    height: int = image.size[1]

    for x in range(width):
        for y in range(height):
            pixel: float | tuple[int, ...] | None = image.getpixel((x, y))

            if not isinstance(pixel, tuple):
                print(f"{Fore.RED}Erreur format pixels.{Fore.RESET}")
                return image

            new_color: tuple[int, ...] = tuple(
                max(0, min(255, int(c * luminosity))) for c in pixel
            )
            image.putpixel((x, y), new_color)

    return image


def convert_image_width(
    image: Image.Image,
    paper_width: float,
    for_landscape_mode: bool = True,
) -> tuple[int, int]:
    width: int = image.size[0]
    height: int = image.size[1]
    aspect_ratio: float = width / height

    if for_landscape_mode:
        new_width: int = int(paper_width * PRINTER_DPI)
        new_height: int = int(new_width / aspect_ratio)
    else:
        new_height: int = int(paper_width * PRINTER_DPI)
        new_width: int = int(new_height / aspect_ratio)

    return (new_width, new_height)


def parse_cfg_for_width(parser: cfgp.ConfigParser) -> float:
    res: float = 0.0
    try:
        parser.read("config.cfg")
    except Exception as error:
        print(f"{Fore.RED}config.cfg introuvable.\nErreur: {error}{Fore.RESET}")
        return res

    try:
        res = parser.getfloat("Settings", "PAPER_WIDTH")
    except Exception as error:
        print(f"{Fore.RED}Erreur lecture config.cfg.\nErreur: {error}{Fore.RESET}")

    return res


if __name__ == "__main__":
    print(f"{Fore.RED}Erreur:\nLe script à exécuter est main.py.")
