import sys
import qtui


class GuiHandler:
    def __init__(self) -> None:
        self.app: qtui.QtWidgets.QApplication
        self.window: qtui.QtWidgets.QMainWindow
        self.ui: qtui.Ui_PrinterGUI


def main() -> None:
    gui: GuiHandler = gui_init()

    gui.ui.image_frame.setPixmap(qtui.QtGui.QPixmap("samples/sample.jpg"))

    run(gui)


def gui_init() -> GuiHandler:
    gui: GuiHandler = GuiHandler()
    gui.app = qtui.QtWidgets.QApplication(sys.argv)
    gui.window = qtui.QtWidgets.QMainWindow()

    gui.ui = qtui.Ui_PrinterGUI()
    gui.ui.setupUi(gui.window)
    return gui


def run(gui: GuiHandler):
    gui.window.show()
    sys.exit(gui.app.exec())


if __name__ == "__main__":
    main()
