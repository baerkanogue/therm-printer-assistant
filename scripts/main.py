import printer as pt


def main() -> None:
    path: str = ""
    open_img_value: pt.Image.Image | None = None

    while not open_img_value:
        path: str = pt.get_image_path()
        open_img_value = pt.open_image(path)

    img: pt.Image.Image = open_img_value
    paper_width: float = pt.get_paper_width()

    img = pt.img_convert_rgb(img)

    img = img.resize(pt.convert_image_width(img, paper_width, pt.is_landscape_select()))

    image: pt.ImageData = pt.ImageData(img, path)

    main_loop(image)


def main_loop(img: pt.ImageData) -> None:
    do_again: bool = True
    output_suffix: int = 0
    while do_again:
        new_image: pt.Image.Image = img.img.copy()
        new_image = pt.change_luminosity(new_image, pt.ask_brightness_level())
        new_image = pt.dither(new_image)

        pt.save_image(new_image, img.path, output_suffix)
        output_suffix += 1

        do_again = pt.ask_quit()

    print(f"{pt.Fore.YELLOW}Fermeture...{pt.Fore.RESET}")


if __name__ == "__main__":
    main()
