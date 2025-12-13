type: ignore[attr - defined]

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from os.path import join


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initialization()
        self.config()

    def config(self) -> None:
        self.save_button.clicked.connect(self.on_run)

    def initialization(self) -> None:
        self.setWindowTitle("Printer")
        ui_path = join("qt", "main.ui")
        uic.loadUi(ui_path, self)

    def on_run(self) -> None:
        print("Button clicked")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
