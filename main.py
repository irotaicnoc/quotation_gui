import sys
import qdarktheme
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea,
                             QLabel, QFrame, QMessageBox, QToolButton, QTabBar, QStackedWidget, QLineEdit, QSpinBox,
                             QDoubleSpinBox, QComboBox, QGridLayout, QFileDialog)

import utils
import calculator
import data_manager
from localization import translate, set_language


class CollapsibleBox(QWidget):
    def __init__(self, title_key="", title_args=None, parent=None, with_browse=False):
        super().__init__(parent)
        self.title_key = title_key
        self.title_args = title_args or []
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_button = QToolButton(checkable=True, checked=True)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.setObjectName("collapsible_header")
        self.toggle_button.toggled.connect(self.on_toggled)
        header_layout.addWidget(self.toggle_button)

        self.browse_btn = None
        if with_browse:
            self.browse_btn = QPushButton()
            header_layout.addWidget(self.browse_btn)

        header_layout.addStretch()

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 10, 0, 15)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(header_layout)
        layout.addWidget(self.content_area)

        self.retranslate_ui()

    def on_toggled(self, checked):
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        self.content_area.setVisible(checked)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

    def retranslate_ui(self):
        title_text = f"{translate(self.title_key)} {' '.join(self.title_args)}" if self.title_args else translate(self.title_key)
        self.toggle_button.setText(title_text)
        if self.browse_btn:
            self.browse_btn.setText(translate("browse"))

        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if hasattr(widget, "retranslate_ui"):
                widget.retranslate_ui()


class ManufacturerGrid(QFrame):
    def __init__(self, manufacturer_name):
        super().__init__()
        self.manufacturer_name = manufacturer_name
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

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
        self.header_labels = []

        header_keys = ["name", "spec1", "spec2", "price", "quantity", "subtotal", "empty"]
        for col, key in enumerate(header_keys):
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if col > 2 else Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(lbl, 0, col)
            self.header_labels.append((lbl, key))

        self.add_btn = QPushButton()
        self.add_btn.setObjectName("add_row_btn")
        self.main_layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_btn.clicked.connect(self.add_row)

        self.retranslate_ui()

    def add_row(self, data=None):
        name_edit = QLineEdit()
        spec1_combo = QComboBox()
        spec1_combo.setStyleSheet(utils.load_stylesheet("menu_style.qss"))
        spec1_combo.addItems(["", "Type A", "Type B", "Type C"])
        spec2_combo = QComboBox()
        spec2_combo.setStyleSheet(utils.load_stylesheet("menu_style.qss"))
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
        del_btn.setObjectName("delete_row_btn")

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
            for _widget in row_widgets:
                self.grid_layout.removeWidget(_widget)
                _widget.deleteLater()
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

    def retranslate_ui(self):
        for lbl, key in self.header_labels:
            if key != "empty":
                lbl.setText(f"<b>{translate(key)}</b>")
        self.add_btn.setText(translate("add_row"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_counter = 1
        self.tab_grids = {}
        self.tab_base_names = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(5)

        self.tab_bar = QTabBar()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setExpanding(False)
        # Widget-level style overrides app-level qdarktheme styles
        self.tab_bar.setStyleSheet(utils.load_stylesheet("tab_style.qss"))
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.add_btn = QToolButton()
        self.add_btn.setText("+")
        self.add_btn.setObjectName("add_tab_btn")
        self.add_btn.clicked.connect(lambda checked: self.add_new_tab())

        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.add_btn)
        tab_layout.addStretch()

        self.lbl_theme = QLabel()
        tab_layout.addWidget(self.lbl_theme)

        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet(utils.load_stylesheet("menu_style.qss"))
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        tab_layout.addWidget(self.theme_combo)

        self.lbl_lang = QLabel()
        tab_layout.addWidget(self.lbl_lang)

        self.lang_combo = QComboBox()
        self.lang_combo.setStyleSheet(utils.load_stylesheet("menu_style.qss"))
        self.lang_combo.addItems(["English", "Italiano"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        tab_layout.addWidget(self.lang_combo)

        main_layout.addLayout(tab_layout)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.add_new_tab(base_key="industrial_plant", number=1)
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 5, 0, 0)

        self.btn_load = QPushButton()
        self.btn_load.clicked.connect(self.handle_load)

        self.btn_save = QPushButton()
        self.btn_save.clicked.connect(self.handle_save)

        self.btn_calc = QPushButton()
        self.btn_calc.setObjectName("calc_btn")
        self.btn_calc.clicked.connect(self.run_calculations)

        bottom_layout.addWidget(self.btn_load)
        bottom_layout.addWidget(self.btn_save)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_calc)

        main_layout.addLayout(bottom_layout)

        self.resize(1000, 650)
        self.retranslate_ui()

    @staticmethod
    def apply_theme(t):
        theme_map = {translate("system"): "auto", translate("light"): "light", translate("dark"): "dark"}
        theme_name = theme_map.get(t, "auto")

        qdarktheme.setup_theme(
            theme_name,
            corner_shape="rounded",
            custom_colors={"primary": "#3B82F6"},
            additional_qss=utils.load_stylesheet("style.qss"),
        )

    def change_language(self, index):
        lang_code = "en" if index == 0 else "it"
        set_language(lang_code)
        self.retranslate_ui()

    def add_new_tab(self, base_key="industrial_plant", number=None):
        if number is None:
            number = self.tab_counter

        new_content, grids_dict = self.create_tab_content()
        self.stack.addWidget(new_content)

        tab_name = f"{translate(base_key)} {number}"
        index = self.tab_bar.addTab(tab_name)

        self.tab_grids[index] = grids_dict
        self.tab_base_names[index] = (base_key, number)

        self.tab_bar.setCurrentIndex(index)
        self.tab_counter += 1

    def change_tab(self, index):
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def close_tab(self, index):
        tab_name = self.tab_bar.tabText(index)
        msg_text = translate("close_prompt").replace("{tab_name}", tab_name)

        reply = QMessageBox.question(
            self,
            translate("confirm"),
            msg_text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

        if reply == QMessageBox.StandardButton.Yes:
            self.tab_bar.removeTab(index)
            widget_to_remove = self.stack.widget(index)
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

            new_tab_grids = {}
            new_tab_base_names = {}
            for i in range(self.tab_bar.count()):
                new_idx = i if i < index else i + 1
                new_tab_grids[i] = self.tab_grids[new_idx]
                new_tab_base_names[i] = self.tab_base_names[new_idx]

            self.tab_grids = new_tab_grids
            self.tab_base_names = new_tab_base_names

    @staticmethod
    def create_tab_content():
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 10, 15, 10)
        content_layout.setSpacing(15)

        grids_dict = {}

        for prod in range(1, 4):
            prod_name = f"Product {prod}"
            prod_box = CollapsibleBox("product", [str(prod)], with_browse=True)
            prod_box.toggle_button.setObjectName("product_header")
            content_layout.addWidget(prod_box)

            grids_dict[prod_name] = []

            for man in range(1, 3):
                man_name = f"Manufacturer {prod}.{man}"
                man_box = CollapsibleBox("manufacturer", [f"{prod}.{man}"])
                man_box.toggle_button.setObjectName("manufacturer_header")
                prod_box.add_widget(man_box)

                grid = ManufacturerGrid(man_name)
                grid.add_row()
                man_box.add_widget(grid)
                grids_dict[prod_name].append(grid)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        return scroll, grids_dict

    def handle_save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, translate("save_dialog"), "", "JSON Files (*.json)")
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
        file_path, _ = QFileDialog.getOpenFileName(self, translate("load_dialog"), "", "JSON Files (*.json)")
        if not file_path:
            return

        try:
            app_data = data_manager.load_from_json(file_path)
        except Exception as e:
            QMessageBox.critical(self, translate("error"), f"{translate('could_not_load')}{e}")
            return

        while self.tab_bar.count() > 0:
            self.tab_bar.removeTab(0)
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
        self.tab_grids.clear()
        self.tab_base_names.clear()

        for tab_info in app_data:
            self.add_new_tab(base_key="industrial_plant", number=self.tab_counter)
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

        result_text = f"<b>{translate('plant_totals')}</b><br>"
        for plant, total in plant_totals.items():
            result_text += f"{plant}: ${total:,.2f}<br>"

        result_text += f"<br><b>{translate('grand_total')} ${grand_total:,.2f}</b>"

        msg = QMessageBox(self)
        msg.setWindowTitle(translate("calc_results"))
        msg.setText(result_text)
        msg.exec()

    def retranslate_ui(self):
        self.setWindowTitle(translate("app_title"))
        self.lbl_theme.setText(translate("theme"))
        self.lbl_lang.setText(translate("language"))

        current_theme_idx = self.theme_combo.currentIndex()
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()
        self.theme_combo.addItems([translate("system"), translate("light"), translate("dark")])
        self.theme_combo.setCurrentIndex(current_theme_idx if current_theme_idx >= 0 else 0)
        self.theme_combo.blockSignals(False)

        self.btn_load.setText(translate("load_config"))
        self.btn_save.setText(translate("save_data"))
        self.btn_calc.setText(translate("run_calc"))

        for i in range(self.tab_bar.count()):
            base_key, number = self.tab_base_names.get(i, ("industrial_plant", i+1))
            self.tab_bar.setTabText(i, f"{translate(base_key)} {number}")

        for i in range(self.stack.count()):
            scroll_area = self.stack.widget(i)
            content_widget = scroll_area.widget()
            layout = content_widget.layout()
            for j in range(layout.count()):
                item = layout.itemAt(j)
                if item.widget() and hasattr(item.widget(), "retranslate_ui"):
                    item.widget().retranslate_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme(
        "auto",
        corner_shape="rounded",
        custom_colors={"primary": "#3B82F6"},
        additional_qss=utils.load_stylesheet("style.qss"),
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
