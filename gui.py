import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QScrollArea,
                             QLabel, QFrame, QMessageBox, QToolButton,
                             QTabBar, QStackedWidget, QSizePolicy,
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QGridLayout)
from PyQt6.QtCore import Qt

class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None, with_browse=False):
        super().__init__(parent)

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
    def __init__(self):
        super().__init__()
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

        headers = ["Name", "Spec 1", "Spec 2", "Price", "Quantity", "Sub-total", ""]
        for col, header in enumerate(headers):
            lbl = QLabel(f"<b>{header}</b>")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if col > 2 else Qt.AlignmentFlag.AlignLeft)
            self.grid_layout.addWidget(lbl, 0, col)

        self.add_row()

        self.add_btn = QPushButton("+ Add Row")
        self.main_layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.add_btn.clicked.connect(self.add_row)

    def add_row(self):
        name_edit = QLineEdit()
        spec1_combo = QComboBox()
        spec1_combo.addItems(["Type A", "Type B", "Type C"])
        spec2_combo = QComboBox()
        spec2_combo.addItems(["Material X", "Material Y", "Material Z"])
        price_box = QDoubleSpinBox()
        price_box.setMaximum(999999.99)
        price_box.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        qty_box = QSpinBox()
        qty_box.setMaximum(9999)
        subtotal_box = QLineEdit("0.00")
        subtotal_box.setReadOnly(True)
        subtotal_box.setStyleSheet("background-color: #e0e0e0; color: #555555;")

        del_btn = QPushButton("X")
        del_btn.setFixedWidth(30)
        del_btn.setStyleSheet("color: red; font-weight: bold;")

        row_widgets = [name_edit, spec1_combo, spec2_combo, price_box, qty_box, subtotal_box, del_btn]

        current_row_idx = self.row_counter
        self.row_counter += 1

        for col, widget in enumerate(row_widgets):
            self.grid_layout.addWidget(widget, current_row_idx, col)

        def update_subtotal(val, p=price_box, q=qty_box, s=subtotal_box):
            total = p.value() * q.value()
            s.setText(f"{total:.2f}")

        def delete_this_row():
            for widget in row_widgets:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

        price_box.valueChanged.connect(update_subtotal)
        qty_box.valueChanged.connect(update_subtotal)
        del_btn.clicked.connect(delete_this_row)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App UI Schema")
        self.resize(950, 600) # Reduced width from 1100 to 950
        self.tab_counter = 1

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

        main_layout.addLayout(tab_layout)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.add_new_tab(name="Industrial Plant 1")

        bottom_layout = QHBoxLayout()
        btn1 = QPushButton("Load Configuration")
        btn2 = QPushButton("Save Data")
        btn3 = QPushButton("Run Calculations")

        bottom_layout.addWidget(btn1)
        bottom_layout.addWidget(btn2)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn3)

        main_layout.addLayout(bottom_layout)

    def add_new_tab(self, checked=False, name=None):
        if not isinstance(name, str):
            name = f"Industrial Plant {self.tab_counter}"

        new_content = self.create_tab_content()
        self.stack.addWidget(new_content)

        index = self.tab_bar.addTab(name)
        self.tab_bar.setCurrentIndex(index)
        self.tab_counter += 1

    def change_tab(self, index):
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def close_tab(self, index):
        tab_name = self.tab_bar.tabText(index)
        reply = QMessageBox.question(
            self, 'Confirm Close', f"Are you sure you want to close {tab_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.tab_bar.removeTab(index)
            widget_to_remove = self.stack.widget(index)
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

    def create_tab_content(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        for prod in range(1, 4):
            prod_box = CollapsibleBox(f"Product {prod}", with_browse=True)
            prod_box.toggle_button.setStyleSheet("QToolButton { border: none; background: transparent; text-align: left; font-size: 16px; font-weight: bold; }")
            content_layout.addWidget(prod_box)

            for man in range(1, 3):
                man_box = CollapsibleBox(f"Manufacturer {prod}.{man}")
                man_box.toggle_button.setStyleSheet("QToolButton { border: none; background: transparent; text-align: left; font-size: 14px; font-weight: bold; color: #333333; }")
                prod_box.add_widget(man_box)

                grid = ManufacturerGrid()
                man_box.add_widget(grid)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        return scroll

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())