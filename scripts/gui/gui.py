import sys
import qtui
import helpers as hp
from os.path import join


class GuiHandler:
    def __init__(self) -> None:
        self.app: qtui.QtWidgets.QApplication
        self.window: qtui.QtWidgets.QMainWindow
        self.ui: qtui.Ui_PrinterGUI

        self.status_label: qtui.QtWidgets.QLabel
        self.working_img: hp.ImageData = hp.ImageData()
        self.output_dir: str

        self._gui_init()
        self._connect()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

    def _gui_init(self) -> None:
        self.app = qtui.QtWidgets.QApplication(sys.argv)
        self.window = qtui.QtWidgets.QMainWindow()
        self.ui = qtui.Ui_PrinterGUI()
        self.ui.setupUi(self.window)

        self.status_label = qtui.QtWidgets.QLabel(self.window)
        stat = self.window.statusBar()
        if stat:
            stat.addPermanentWidget(self.status_label)

        try:
            self.ui.dpi_spin_box.setValue(hp.parse_cfg_for_width())
        except Exception as error:
            self.status_label.setText(f"config.cgf error: {error}")

    def _connect(self) -> None:
        self.ui.save_button.pressed.connect(self._on_save_button_pressed)
        self.ui.preview_button.pressed.connect(self._on_preview_button_pressed)
        self.ui.open_button.pressed.connect(self._on_open_button_pressed)
        self.ui.choose_button.pressed.connect(self._on_choose_button_pressed)

    def _on_preview_button_pressed(self) -> None:
        self._get_queued_process()

    def _on_open_button_pressed(self) -> None:
        file_str: str
        try:
            file_str = qtui.QtWidgets.QFileDialog.getOpenFileName(
                self.window,
                "Select a picture",
                ".",
                "Images (*.png *.jpg *.jpeg);;All Files (*)",
            )[0]
        except Exception as error:
            self.status_label.setText(f"Error: {error}")
            return

        img_open: hp.Image.Image | None = None
        try:
            img_open = hp.Image.open(file_str)
        except Exception as error:
            self.status_label.setText(f"Error: {error}")
            return

        self.ui.file_path_line.setText(file_str)
        self.ui.image_frame.setPixmap(qtui.QtGui.QPixmap(file_str))
        self.working_img.origin_img = img_open
        self.working_img.img = img_open.copy()
        self.working_img.path = file_str

    def _on_choose_button_pressed(self) -> None:
        dir_str: str
        try:
            dir_str = qtui.QtWidgets.QFileDialog.getExistingDirectory(
                self.window,
                "Select a directory",
                ".",
                qtui.QtWidgets.QFileDialog.Option.ShowDirsOnly
                | qtui.QtWidgets.QFileDialog.Option.DontResolveSymlinks,
            )
        except Exception as error:
            self.status_label.setText(f"Error: {error}")
            return

        self.ui.output_path_line.setText(dir_str)
        self.output_dir = dir_str

    def _on_save_button_pressed(self) -> None:
        try:
            file_name: str | None = None
            custom_name: str | None = self.ui.output_name_line.text()
            if custom_name:
                file_name = hp.get_stem(custom_name)
            else:
                file_name = hp.get_stem(self.working_img.path)

            if not file_name:
                self.status_label.setText(f"Error: No file name")
                return
            if not self.output_dir:
                self.status_label.setText(f"Error: No output directory ")
                return

            output_name: str = f"{join(self.output_dir, file_name)}.png"
            if not self.working_img.img:
                self.status_label.setText(f"Error: No image loaded")
                return
            self.working_img.img.save(output_name)
        except Exception as error:
            self.status_label.setText(f"Error: {error}")
            return

        self.status_label.setText(f"Image save: {output_name}")

    def _get_queued_process(self) -> hp.QueuedProcess | None:
        use_dither: bool = bool(self.ui.dither_check_box.checkState().value)

        use_landscape: bool = False
        landscape_str = self.ui.landscape_combo_box.currentText()
        if landscape_str == "landscape":
            use_landscape = True
        elif landscape_str == "portrait":
            use_landscape = False
        else:
            self.status_label.setText(f"Landscape mode error, value: {landscape_str}")
            return

        brightness: float = self.ui.brightness_spin_box.value()
        dpi: float = self.ui.brightness_spin_box.value()

        process: hp.QueuedProcess = hp.QueuedProcess(
            use_dither, use_landscape, brightness, dpi
        )

        return process


if __name__ == "__main__":
    gui: GuiHandler = GuiHandler()
    gui.ui.image_frame.setPixmap(qtui.QtGui.QPixmap("samples/sample.jpg"))
    gui.run()
