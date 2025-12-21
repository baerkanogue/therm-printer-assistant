import ui_info as uii
from helpers import resource_path, Path


class InfoWindow(uii.QtWidgets.QDialog):
    def __init__(self, parent: uii.QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.ui = uii.Ui_Dialog()
        self.ui.setupUi(self)

        logo_path: Path = resource_path("icons/logo.ico")
        logo_icon: str = str(logo_path)
        logo_img: uii.QtGui.QPixmap = uii.QtGui.QPixmap(logo_icon)
        logo_img = logo_img.scaled(
            self.ui.logo_frame.size(),
            uii.QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            uii.QtCore.Qt.TransformationMode.FastTransformation,
        )
        self.ui.logo_frame.setPixmap(logo_img)
