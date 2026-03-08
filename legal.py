import sys
import json
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTextEdit,
                               QHBoxLayout, QPushButton, QWidget, QComboBox)

import utils
import config
import data_manager
from localization import translate


def get_eula_html(file_name: str, lang_code: str = None) -> str:
    """Returns the localized EULA text/HTML."""
    if lang_code is None:
        lang_code = config.CURRENT_LANG

    file_name_no_extension = file_name.split(".")[0]
    file_extension = file_name.split(".")[-1]
    localized_file_name = f"{file_name_no_extension}_{lang_code}.{file_extension}"
    file_path = utils.resource_path(config.LICENSES_FOLDER_PATH / localized_file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return translate("file_not_found_error", file_name=file_path)


def get_third_party_licenses_html(file_name: str) -> str:
    """Reads a JSON license file and formats it into HTML."""
    file_path = utils.resource_path(config.LICENSES_FOLDER_PATH / file_name)
    try:
        raw_data = data_manager.load_from_json(file_path)
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

        return html_content
    except FileNotFoundError:
        return translate("file_not_found_error", file_name=file_path)
    except json.JSONDecodeError:
        return translate("json_error", file_name=file_path)


class TextFileDialog(QDialog):
    def __init__(self,
                 title: str,
                 file_name: str,
                 parent: QWidget = None,
                 readonly: bool = True,
                 is_html_format: bool = False,
                 ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)
        self.setModal(True)

        self.file_name = file_name
        self.is_html_format = is_html_format

        layout = QVBoxLayout(self)
        is_eula = "EULA" in file_name
        if is_eula:
            top_layout = QHBoxLayout()
            if readonly:
                lbl = QLabel(f'{translate("eula_title")}:')
            else:
                lbl = QLabel(translate("eula_accept_label"))
            top_layout.addWidget(lbl)
            top_layout.addStretch()

            # Add Language Dropdown
            self.lang_combo = QComboBox()
            self.lang_combo.setStyleSheet(utils.load_stylesheet(config.MENU_CUSTOM_STYLE_NAME))
            self.lang_combo.addItem("Italiano", "it")
            self.lang_combo.addItem("English", "en")
            language_index = 0  # Italian
            if config.CURRENT_LANG == "en":
                language_index = 1
            self.lang_combo.setCurrentIndex(language_index)

            self.lang_combo.currentIndexChanged.connect(self._reload_eula)
            top_layout.addWidget(self.lang_combo)
            layout.addLayout(top_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        if "THIRDPARTY" in file_name:
            self.text_edit.setHtml(get_third_party_licenses_html(file_name))
        elif is_eula:
            self._reload_eula()
        else:
            # Fallback for any other standard text files
            file_path = utils.resource_path(config.LICENSES_FOLDER_PATH / file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    if is_html_format:
                        self.text_edit.setHtml(f.read())
                    else:
                        self.text_edit.setText(f.read())
            except FileNotFoundError:
                self.text_edit.setText(translate("file_not_found_error", file_name=file_path))

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

    def _reload_eula(self):
        """Reloads the EULA text when the language is changed via the combobox."""
        lang_code = self.lang_combo.currentData()
        content = get_eula_html(self.file_name, lang_code)
        if self.is_html_format:
            self.text_edit.setHtml(content)
        else:
            self.text_edit.setText(content)


def eula_agreement_dialog(initial_eula_dialog: str) -> None:
    # TODO: remove in final version
    assert initial_eula_dialog in ["yes", "no", "auto"]
    if config.INITIAL_EULA_DIALOG == "no":
        return
    settings = QSettings(config.COMPANY_NAME, config.APP_NAME)
    if config.INITIAL_EULA_DIALOG == "yes":
        settings.remove("eula_accepted")
    if not settings.value("eula_accepted", False, type=bool):
        eula_dialog = TextFileDialog(
            title=translate("eula_title"),
            file_name=config.LICENSE_FILE_NAME,
            parent=None,
            readonly=False,
            is_html_format=True,
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

    # Translated descriptive text
    about_content = translate(
        "about_text",
        app_name=config.APP_NAME,
        app_version=config.APP_VERSION,
        year=config.YEAR,
        company_name=config.COMPANY_NAME,
    )

    about_text = QLabel(about_content)
    about_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
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
            is_html_format=True,
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
