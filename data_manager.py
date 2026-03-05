import json
import openpyxl
import pandas as pd
from PySide6.QtCore import Qt
from PIL.ImageQt import ImageQt
from PySide6.QtGui import QPixmap
from openpyxl_image_loader import SheetImageLoader
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QHBoxLayout, QWidget, QCheckBox, QMessageBox, QLabel)

from localization import translate


def save_to_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def load_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


class ProductSelectionDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translate("select_products"))
        self.resize(700, 500)
        self.selected_data = []
        self.load_successful = False

        layout = QVBoxLayout(self)

        # Setup Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Setup Buttons
        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("OK")
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
            # 1. Load data with pandas for text/numbers (header=1 skips the 1st row, using the 2nd as header)
            df = pd.read_excel(file_path, header=1)

            # 2. Load the workbook with openpyxl to extract images
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            image_loader = SheetImageLoader(sheet)

            self.table.setColumnCount(len(df.columns) + 1)
            self.table.setHorizontalHeaderLabels([translate("select")] + list(df.columns))
            self.table.setRowCount(len(df))

            schema_col_idx = df.columns.get_loc("SCHEMA") + 1 if "SCHEMA" in df.columns else -1

            for row_idx, row in df.iterrows():
                # Add Checkbox
                chk_widget = QWidget()
                chk_layout = QHBoxLayout(chk_widget)
                chk_box = QCheckBox()
                chk_layout.addWidget(chk_box)
                chk_layout.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row_idx, 0, chk_widget)

                # Add data and images
                for col_idx, value in enumerate(row):
                    actual_col = col_idx + 1

                    # If this is the SCHEMA column, try to load the image
                    if actual_col == schema_col_idx:
                        # Excel rows are 1-indexed. Header is on row 2, so data starts at row 3
                        excel_cell = f"{openpyxl.utils.get_column_letter(actual_col)}{row_idx + 3}"

                        if image_loader.image_in(excel_cell):
                            # Extract image using PIL
                            pil_img = image_loader.get(excel_cell)

                            # Convert PIL Image to QPixmap
                            q_image = ImageQt(pil_img)
                            pixmap = QPixmap.fromImage(q_image)

                            # Scale pixmap if necessary
                            pixmap = pixmap.scaled(
                                50,
                                50,
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation,
                            )

                            # Place inside a QLabel
                            img_label = QLabel()
                            img_label.setPixmap(pixmap)
                            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                            self.table.setCellWidget(row_idx, actual_col, img_label)
                            self.table.setRowHeight(row_idx, 60)  # Adjust row height to fit image
                        else:
                            self.table.setItem(row_idx, actual_col, QTableWidgetItem("No Image"))
                    else:
                        self.table.setItem(row_idx, actual_col, QTableWidgetItem(str(value)))

            self.load_successful = True

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
