import sys
import json
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QWidget

import utils
import config
import data_manager
from localization import translate


class TextFileDialog(QDialog):
    def __init__(self, title: str, file_name: str, parent: QWidget = None, readonly: bool = False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)

        if "EULA" in file_name:
            if readonly:
                lbl = QLabel(f'{translate("eula_title")}:')
            else:
                lbl = QLabel(translate("eula_accept_label"))
            layout.addWidget(lbl)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Load file
        file_path = utils.resource_path(config.LICENSES_FOLDER_PATH / file_name)
        try:
            if file_name.endswith(".json"):
                raw_data = data_manager.load_from_json(file_path)

                # Convert JSON list to an HTML string
                html_content = ""
                for pkg in raw_data:
                    name = pkg.get("Name", "Unknown Package")
                    version = pkg.get("Version", "")
                    license_name = pkg.get("License", "Unknown License")
                    license_text = pkg.get("LicenseText", "No license text provided.")

                    html_content += f"<h3>{name} (v{version})</h3>"
                    html_content += f"<p><b>License:</b> {license_name}</p>"
                    html_content += f"<pre style='background-color: #2b2b2b; padding: 10px;'>{license_text}</pre>"
                    html_content += "<hr>"

                self.text_edit.setHtml(html_content)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.text_edit.setText(f.read())

        except FileNotFoundError:
            self.text_edit.setText(translate("file_not_found_error", file_name=file_path))
        except json.JSONDecodeError:
            self.text_edit.setText(translate("json_error", file_name=file_path))

        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # Change buttons based on mode
        if readonly:
            self.btn_close = QPushButton(translate("close"))
            btn_layout.addWidget(self.btn_close)
            self.btn_close.clicked.connect(self.accept)
        else:
            self.btn_accept = QPushButton(translate("accept"))
            self.btn_decline = QPushButton(translate("decline"))
            btn_layout.addWidget(self.btn_accept)
            btn_layout.addWidget(self.btn_decline)
            self.btn_accept.clicked.connect(self.accept)
            self.btn_decline.clicked.connect(self.reject)

        layout.addLayout(btn_layout)


def eula_agreement_dialog():
    settings = QSettings(config.COMPANY_NAME, config.APP_NAME)
    # settings.remove("eula_accepted")
    if not settings.value("eula_accepted", False, type=bool):
        eula_dialog = TextFileDialog(
            title=translate("eula_title"),
            file_name=config.LICENSE_FILE_NAME,
            parent=None,
            readonly=False,
        )
        if eula_dialog.exec() == QDialog.DialogCode.Accepted:
            settings.setValue("eula_accepted", True)
        else:
            sys.exit()  # Close app if they decline


def show_about_dialog(parent: QWidget):
    # Create a custom dialog to add the "View EULA" button
    about_dialog = QDialog(parent)
    about_dialog.setWindowTitle(translate("about_title"))
    layout = QVBoxLayout(about_dialog)

    # Combine translated descriptive text with hardcoded libraries and licenses
    about_content = (
            translate(
                "about_text",
                app_name=config.APP_NAME,
                app_version=config.APP_VERSION,
                year=config.YEAR,
                company_name=config.COMPANY_NAME,
            ) +
            "- PySide6 (LGPLv3)<br>"
            "- Pandas, Pillow, Openpyxl-image-loader,"
            "<br> Openpyxl, Jinja2, PyInstaller,"
            "<br> PyQtDarkTheme (MIT/BSD/Apache)"
    )
    about_text = QLabel(about_content)
    layout.addWidget(about_text)

    btn_layout = QHBoxLayout()
    btn_layout.addStretch()

    # View EULA Button
    btn_view_eula = QPushButton(translate("view_eula"))
    btn_view_eula.clicked.connect(
        lambda: TextFileDialog(
            title=translate("eula_title"),
            file_name=config.LICENSE_FILE_NAME,
            parent=parent,
            readonly=True,
        ).exec()
    )
    btn_layout.addWidget(btn_view_eula)

    # View Third-Party Licenses Button
    btn_view_third_party = QPushButton(translate("view_third_party"))
    btn_view_third_party.clicked.connect(
        lambda: TextFileDialog(
            title=translate("view_third_party"),
            file_name=config.THIRD_PARTY_LICENSE_FILE_NAME,
            parent=parent,
            readonly=True,
        ).exec()
    )
    btn_layout.addWidget(btn_view_third_party)

    # Close Button
    btn_close = QPushButton(translate("close"))
    btn_close.clicked.connect(about_dialog.accept)
    btn_layout.addWidget(btn_close)

    layout.addLayout(btn_layout)
    about_dialog.exec()
