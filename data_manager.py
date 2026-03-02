import json
import pandas as pd
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QWidget, QCheckBox, QMessageBox)

from localization import translate


def save_to_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


class ProductSelectionDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translate("select_products"))
        self.resize(700, 500)
        self.selected_data = []

        layout = QVBoxLayout(self)

        # Setup Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Setup Buttons
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton(translate("ok"))
        self.btn_cancel = QPushButton(translate("cancel"))
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        # Connections
        self.btn_ok.clicked.connect(self.accept_selection)
        self.btn_cancel.clicked.connect(self.reject)

        self.load_data(file_path)

    def load_data(self, file_path):
        try:
            df = pd.read_excel(file_path)

            self.table.setColumnCount(len(df.columns) + 1)
            self.table.setHorizontalHeaderLabels([translate("select")] + list(df.columns))
            self.table.setRowCount(len(df))

            # Populate table
            for row_idx, row in df.iterrows():
                # Add Checkbox in column 0
                chk_widget = QWidget()
                chk_layout = QHBoxLayout(chk_widget)
                chk_box = QCheckBox()
                chk_layout.addWidget(chk_box)
                chk_layout.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row_idx, 0, chk_widget)

                # Add data
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx + 1, QTableWidgetItem(str(value)))

        except Exception as e:
            error_title = translate("error")
            error_msg = f"{translate('error_loading_file')} {file_path}:\n\n{str(e)}"
            QMessageBox.critical(self, error_title, error_msg)

    def accept_selection(self):
        self.selected_data = []
        for row in range(self.table.rowCount()):
            # Retrieve checkbox state
            chk_widget = self.table.cellWidget(row, 0)
            chk_box = chk_widget.layout().itemAt(0).widget()

            if chk_box.isChecked():
                row_data = {}
                # Extract headers and values for checked rows
                for col in range(1, self.table.columnCount()):
                    header = self.table.horizontalHeaderItem(col).text()
                    item = self.table.item(row, col)
                    row_data[header] = item.text() if item else ""
                self.selected_data.append(row_data)

        self.accept()
