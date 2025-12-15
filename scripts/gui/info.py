import ui_info as uii
from helpers import resource_path, Path


class InfoWindow(uii.QtWidgets.QDialog):
    def __init__(self, parent: uii.QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.ui = uii.Ui_Dialog()
        self.ui.setupUi(self)

        logo_path: Path = resource_path("icons/logo.ico")
        logo_icon: str = str(logo_path)
        self.ui.logo_label.setPixmap(uii.QtGui.QPixmap(logo_icon))
