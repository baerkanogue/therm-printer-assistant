import sys
import info
import helpers as hp
import ui_main as uim
from os import remove
from os.path import join


class GuiHandler:
    def __init__(self) -> None:
        self.app: uim.QtWidgets.QApplication
        self.window: uim.QtWidgets.QMainWindow
        self.ui: uim.Ui_PrinterGUI

        self.status_label: uim.QtWidgets.QLabel
        self.working_img: hp.ImageData = hp.ImageData()
        self.output_dir: str = "."
        self.config: hp.Config | None = None

        self.default_image: hp.ImageData = hp.ImageData()

        self._gui_init()
        self._connect()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

    def _gui_init(self) -> None:
        self.app = uim.QtWidgets.QApplication(sys.argv)
        self.window = uim.QtWidgets.QMainWindow()

        self.ui = uim.Ui_PrinterGUI()
        self.ui.setupUi(self.window)

        self.window.setWindowTitle("ThermPrinter Assistant")
        win_icon_path: hp.Path = hp.resource_path("icons/printer3d.ico")
        win_icon: uim.QtGui.QIcon = uim.QtGui.QIcon(str(win_icon_path))
        self.window.setWindowIcon(win_icon)

        self.status_label = uim.QtWidgets.QLabel(self.window)
        stat = self.window.statusBar()
        if stat:
            stat.addPermanentWidget(self.status_label)

        try:
            self.config = hp.parse_cfg()
            self.ui.dpi_spin_box.setValue(self.config.dpi)
            self.ui.width_spin_box.setValue(self.config.width)
        except Exception as error:
            print(f"config.cfg error: {error}")

        sample_path: hp.Path = hp.resource_path("samples/sample.jpg")
        self.default_image.path = str(sample_path)
        self.default_image.img = hp.Image.open(self.default_image.path)
        self.default_image.origin_img = self.default_image.img

        self.working_img = self.default_image

        self.ui.image_frame.setPixmap(uim.QtGui.QPixmap(self.working_img.path))

    def _connect(self) -> None:
        self.ui.save_button.pressed.connect(self._on_save_button_pressed)
        self.ui.preview_button.pressed.connect(self._on_preview_button_pressed)
        self.ui.open_button.pressed.connect(self._on_open_button_pressed)
        self.ui.choose_button.pressed.connect(self._on_choose_button_pressed)
        self.ui.info_button.pressed.connect(self._on_info_button_pressed)

    def _on_preview_button_pressed(self) -> None:
        proc: hp.QueuedProcess | None = self._get_queued_process()
        if not proc:
            self.status_label.setText("Error getting process parameters")
            return
        try:
            self.working_img.img = hp.process_image(self.working_img.origin_img, proc)
            self.working_img.tmp = ".tmp.png"

            self.working_img.img.save(self.working_img.tmp)
            tmp_img: uim.QtGui.QPixmap = uim.QtGui.QPixmap(self.working_img.tmp)
            tmp_img = tmp_img.scaled(
                self.ui.image_frame.size(),
                uim.QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                uim.QtCore.Qt.TransformationMode.FastTransformation,
            )
            gui.ui.image_frame.setPixmap(tmp_img)

            try:
                remove(self.working_img.tmp)
            except Exception as error:
                self.status_label.setText(f"{error}")

        except Exception as error:
            self.status_label.setText(f"Processing error: {error}")

    def _on_open_button_pressed(self) -> None:
        file_str: str
        try:
            file_str = uim.QtWidgets.QFileDialog.getOpenFileName(
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
        self.ui.image_frame.setPixmap(uim.QtGui.QPixmap(file_str))
        self.working_img.origin_img = img_open
        self.working_img.img = img_open.copy()
        self.working_img.path = file_str

    def _on_choose_button_pressed(self) -> None:
        dir_str: str
        try:
            dir_str = uim.QtWidgets.QFileDialog.getExistingDirectory(
                self.window,
                "Select a directory",
                ".",
                uim.QtWidgets.QFileDialog.Option.ShowDirsOnly
                | uim.QtWidgets.QFileDialog.Option.DontResolveSymlinks,
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
                self.output_dir = "."

            output_name: str = f"{join(self.output_dir, file_name)}.png"
            if not self.working_img.img:
                self.status_label.setText(f"Error: No image loaded")
                return
            self.working_img.img.save(output_name)
        except Exception as error:
            self.status_label.setText(f"Error: {error}")
            return

        self.status_label.setText(f"Image save: {output_name}")

    def _on_info_button_pressed(self) -> None:
        dlg = info.InfoWindow(self.window)
        dlg.exec()

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

        dpi: int = self.ui.dpi_spin_box.value()
        width: float = self.ui.width_spin_box.value()
        contrast: float = self.ui.contrast_spin_box.value()
        brightness: float = self.ui.brightness_spin_box.value()

        process: hp.QueuedProcess = hp.QueuedProcess(
            dpi, width, contrast, brightness, use_landscape, use_dither
        )

        return process


if __name__ == "__main__":
    gui: GuiHandler = GuiHandler()
    gui.run()
