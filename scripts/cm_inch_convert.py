from colorama import Fore


def convert() -> None:
    cm: float = 0.0
    CM_TO_INCH_RATIO: float = 0.39370079

    while not cm:
        try:
            cm = float(input(f"{Fore.YELLOW}Mesure en centimètres:{Fore.RESET} "))
        except Exception as error:
            print(f"{Fore.RED}Erreur:{Fore.RESET} {error}")

    print(f"{Fore.GREEN}Mesure en pouces:{Fore.RESET} {cm * CM_TO_INCH_RATIO}")


def main() -> None:
    is_looping: bool = True
    while is_looping:
        convert()
        is_loop_str: str = ""
        while is_loop_str != "y" and is_loop_str != "n":
            is_loop_str = input(f"{Fore.YELLOW}Recommencer ? Y/N:{Fore.RESET} ").lower()
        is_looping = False if is_loop_str == "n" else True
    print(f"{Fore.YELLOW}Fermeture...{Fore.RESET}")


if __name__ == "__main__":
    main()
