import sys
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QWidget

import utils
import config

class EULADialog(QDialog):
    def __init__(self, parent=None, readonly=False):
        super().__init__(parent)
        self.setWindowTitle("End User License Agreement")
        self.resize(600, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Change label based on mode
        if readonly:
            lbl = QLabel("End User License Agreement:")
        else:
            lbl = QLabel("Please read and accept the EULA to continue:")
        layout.addWidget(lbl)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Load EULA from file
        eula_path = utils.resource_path(config.licenses_folder_path / config.license_file_name)
        try:
            with open(eula_path, "r", encoding="utf-8") as f:
                eula_text = f.read()
        except FileNotFoundError:
            eula_text = (f"Error: {config.license_file_name} not found. Please ensure"
                         f" the license file is included with the application.")

        self.text_edit.setText(eula_text)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # Change buttons based on mode
        if readonly:
            self.btn_close = QPushButton("Close")
            btn_layout.addWidget(self.btn_close)
            self.btn_close.clicked.connect(self.accept)
        else:
            self.btn_accept = QPushButton("Accept")
            self.btn_decline = QPushButton("Decline")
            btn_layout.addWidget(self.btn_accept)
            btn_layout.addWidget(self.btn_decline)
            self.btn_accept.clicked.connect(self.accept)
            self.btn_decline.clicked.connect(self.reject)

        layout.addLayout(btn_layout)


def eula_agreement_dialog():
    settings = QSettings("YourCompany", "YourApp")
    if not settings.value("eula_accepted", False, type=bool):
        eula_dialog = EULADialog(readonly=False)
        if eula_dialog.exec() == QDialog.DialogCode.Accepted:
            settings.setValue("eula_accepted", True)
        else:
            sys.exit()  # Close app if they decline


def show_about_dialog(parent: QWidget):
    # Create a custom dialog to add the "View EULA" button
    about_dialog = QDialog(parent)
    about_dialog.setWindowTitle("About")
    layout = QVBoxLayout(about_dialog)

    about_text = QLabel(
        "<b>App Name v1.0</b><br>"
        "© 2026 Your Company Name. All rights reserved.<br><br>"
        "<i>Third-party credits (and their dependencies):</i><br>"
        "- PySide6 (LGPLv3)<br>"
        "- Pandas, Openpyxl, Openpyxl-image-loader, Pillow, Jinja2, PyInstaller, PyQtDarkTheme (MIT/BSD/Apache)"
    )
    layout.addWidget(about_text)
    btn_layout = QHBoxLayout()
    btn_layout.addStretch()

    btn_view_eula = QPushButton("View EULA")
    # Open EULA dialog in readonly mode
    eula_dialog = EULADialog(parent, readonly=True)
    btn_view_eula.clicked.connect(lambda: eula_dialog.exec())
    btn_layout.addWidget(btn_view_eula)

    btn_close = QPushButton("Close")
    btn_close.clicked.connect(about_dialog.accept)
    btn_layout.addWidget(btn_close)

    layout.addLayout(btn_layout)
    about_dialog.exec()
