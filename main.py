import sys
import qdarktheme
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea,
                             QLabel, QFrame, QMessageBox, QToolButton, QTabBar, QStackedWidget, QLineEdit, QSpinBox,
                             QDoubleSpinBox, QComboBox, QGridLayout, QFileDialog)

import data_manager
import calculator


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None, with_browse=False):
        super().__init__(parent)
        self.title = title
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=True)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.setStyleSheet("QToolButton { border: none; background: transparent; text-align: left; }")
        self.toggle_button.toggled.connect(self.on_toggled)
        header_layout.addWidget(self.toggle_button)

        if with_browse:
            self.browse_btn = QPushButton("Browse")
            header_layout.addWidget(self.browse_btn)

        header_layout.addStretch()

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 5, 0, 15)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(header_layout)
        layout.addWidget(self.content_area)

    def on_toggled(self, checked):
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        self.content_area.setVisible(checked)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)


class ManufacturerGrid(QFrame):
    def __init__(self, manufacturer_name):
        super().__init__()
        self.manufacturer_name = manufacturer_name
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.grid_layout.setColumnStretch(0, 3)
        self.grid_layout.setColumnStretch(1, 2)
        self.grid_layout.setColumnStretch(2, 2)
        self.grid_layout.setColumnStretch(3, 1)
        self.grid_layout.setColumnStretch(4, 1)
        self.grid_layout.setColumnStretch(5, 1)
        self.grid_layout.setColumnStretch(6, 0)

        self.row_counter = 1
        self.active_rows = []

        headers = ["Name", "Spec 1", "Spec 2", "Price", "Quantity", "Sub-total", ""]
        for col, header in enumerate(headers):
            lbl = QLabel(f"<b>{header}</b>")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if col > 2 else Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(lbl, 0, col)

        self.add_btn = QPushButton("+ Add Row")
        self.main_layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_btn.clicked.connect(self.add_row)

    def add_row(self, data=None):
        name_edit = QLineEdit()
        spec1_combo = QComboBox()
        spec1_combo.addItems(["", "Type A", "Type B", "Type C"])
        spec2_combo = QComboBox()
        spec2_combo.addItems(["", "Material X", "Material Y", "Material Z"])
        price_box = QDoubleSpinBox()
        price_box.setMaximum(999999.99)
        price_box.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        qty_box = QSpinBox()
        qty_box.setMaximum(9999)
        subtotal_box = QLineEdit("0.00")
        subtotal_box.setReadOnly(True)

        del_btn = QPushButton("X")
        del_btn.setFixedWidth(30)
        del_btn.setStyleSheet("color: #ff5555; font-weight: bold;")

        if data:
            name_edit.setText(data.get("name", ""))
            spec1_combo.setCurrentText(data.get("spec1", ""))
            spec2_combo.setCurrentText(data.get("spec2", ""))
            price_box.setValue(data.get("price", 0.0))
            qty_box.setValue(data.get("qty", 0))

        row_widgets = [name_edit, spec1_combo, spec2_combo, price_box, qty_box, subtotal_box, del_btn]

        current_row_idx = self.row_counter
        self.row_counter += 1

        for col, widget in enumerate(row_widgets):
            self.grid_layout.addWidget(widget, current_row_idx, col)

        row_dict = {
            'name': name_edit,
            'spec1': spec1_combo,
            'spec2': spec2_combo,
            'price': price_box,
            'qty': qty_box,
            'widgets': row_widgets,
            'del_btn': del_btn,
        }
        self.active_rows.append(row_dict)

        def update_subtotal(*args):
            s = price_box.value() * qty_box.value()
            subtotal_box.setText(f"{s:.2f}")

        def delete_this_row():
            for widget in row_widgets:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()
            if row_dict in self.active_rows:
                self.active_rows.remove(row_dict)

        price_box.valueChanged.connect(update_subtotal)
        qty_box.valueChanged.connect(update_subtotal)
        del_btn.clicked.connect(delete_this_row)

        update_subtotal()
        return row_dict

    def get_data(self):
        rows_data = []
        for row in self.active_rows:
            rows_data.append({
                "name": row['name'].text(),
                "spec1": row['spec1'].currentText(),
                "spec2": row['spec2'].currentText(),
                "price": row['price'].value(),
                "qty": row['qty'].value()
            })
        return {self.manufacturer_name: rows_data}

    def clear_rows(self):
        for row in list(self.active_rows):
            row['del_btn'].click()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App UI Schema")
        self.resize(950, 600)
        self.tab_counter = 1
        self.tab_grids = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(2)

        self.tab_bar = QTabBar()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.add_btn = QToolButton()
        self.add_btn.setText("+")
        self.add_btn.clicked.connect(self.add_new_tab)

        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.add_btn)
        tab_layout.addStretch()

        # --- Theme Switcher ---
        tab_layout.addWidget(QLabel("Theme:"))
        theme_combo = QComboBox()
        theme_combo.addItems(["System", "Light", "Dark"])
        theme_combo.currentTextChanged.connect(
            lambda t: qdarktheme.setup_theme("auto" if t == "System" else t.lower())
        )
        tab_layout.addWidget(theme_combo)

        main_layout.addLayout(tab_layout)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.add_new_tab(name="Industrial Plant 1")
        bottom_layout = QHBoxLayout()

        btn_load = QPushButton("Load Configuration")
        btn_load.clicked.connect(self.handle_load)

        btn_save = QPushButton("Save Data")
        btn_save.clicked.connect(self.handle_save)

        btn_calc = QPushButton("Run Calculations")
        btn_calc.clicked.connect(self.run_calculations)

        bottom_layout.addWidget(btn_load)
        bottom_layout.addWidget(btn_save)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn_calc)

        main_layout.addLayout(bottom_layout)

    def add_new_tab(self, name=None):
        if not isinstance(name, str):
            name = f"Industrial Plant {self.tab_counter}"

        new_content, grids_dict = self.create_tab_content()
        self.stack.addWidget(new_content)

        index = self.tab_bar.addTab(name)
        self.tab_grids[index] = grids_dict
        self.tab_bar.setCurrentIndex(index)
        self.tab_counter += 1

    def change_tab(self, index):
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def close_tab(self, index):
        tab_name = self.tab_bar.tabText(index)
        reply = QMessageBox.question(
            self,
            'Confirm',
            f"Close {tab_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.tab_bar.removeTab(index)
            widget_to_remove = self.stack.widget(index)
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

            new_tab_grids = {}
            for i in range(self.tab_bar.count()):
                new_tab_grids[i] = self.tab_grids[i if i < index else i + 1]
            self.tab_grids = new_tab_grids

    @staticmethod
    def create_tab_content():
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        grids_dict = {}

        for prod in range(1, 4):
            prod_name = f"Product {prod}"
            prod_box = CollapsibleBox(prod_name, with_browse=True)
            prod_box.toggle_button.setStyleSheet("QToolButton { border: none; background: transparent; "
                                                 "text-align: left; font-size: 16px; font-weight: bold; }")
            content_layout.addWidget(prod_box)

            grids_dict[prod_name] = []

            for man in range(1, 3):
                man_name = f"Manufacturer {prod}.{man}"
                man_box = CollapsibleBox(man_name)
                man_box.toggle_button.setStyleSheet("QToolButton { border: none; background: transparent; text-align: "
                                                    "left; font-size: 14px; font-weight: bold; }")
                prod_box.add_widget(man_box)

                grid = ManufacturerGrid(man_name)
                grid.add_row()
                man_box.add_widget(grid)
                grids_dict[prod_name].append(grid)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        return scroll, grids_dict

    def handle_save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json)")
        if not file_path:
            return

        app_data = []
        for index in range(self.tab_bar.count()):
            tab_data = {"tab_name": self.tab_bar.tabText(index), "products": {}}
            grids_dict = self.tab_grids[index]

            for prod_name, grid_list in grids_dict.items():
                tab_data["products"][prod_name] = {}
                for grid in grid_list:
                    tab_data["products"][prod_name].update(grid.get_data())
            app_data.append(tab_data)

        data_manager.save_to_json(file_path, app_data)

    def handle_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json)")
        if not file_path:
            return

        try:
            app_data = data_manager.load_from_json(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load file:\n{e}")
            return

        while self.tab_bar.count() > 0:
            self.tab_bar.removeTab(0)
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
        self.tab_grids.clear()

        for tab_info in app_data:
            self.add_new_tab(name=tab_info["tab_name"])
            current_index = self.tab_bar.count() - 1
            grids_dict = self.tab_grids[current_index]

            for prod_name, manufacturers in tab_info["products"].items():
                grid_list = grids_dict.get(prod_name, [])

                for grid in grid_list:
                    grid.clear_rows()
                    man_data = manufacturers.get(grid.manufacturer_name, [])
                    for row_data in man_data:
                        grid.add_row(row_data)

    def run_calculations(self):
        app_data = []
        for index in range(self.tab_bar.count()):
            tab_data = {"tab_name": self.tab_bar.tabText(index), "products": {}}
            grids_dict = self.tab_grids[index]

            for prod_name, grid_list in grids_dict.items():
                tab_data["products"][prod_name] = {}
                for grid in grid_list:
                    tab_data["products"][prod_name].update(grid.get_data())
            app_data.append(tab_data)

        plant_totals, grand_total = calculator.calculate_totals(app_data)

        result_text = "<b>Industrial Plant Totals:</b><br>"
        for plant, total in plant_totals.items():
            result_text += f"{plant}: ${total:,.2f}<br>"

        result_text += f"<br><b>Grand Total: ${grand_total:,.2f}</b>"

        msg = QMessageBox(self)
        msg.setWindowTitle("Calculation Results")
        msg.setText(result_text)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")  # Starts with the system default theme
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
