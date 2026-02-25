import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QScrollArea,
                             QLabel, QFrame, QMessageBox, QToolButton,
                             QTabBar, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt

class CollapsibleBox(QWidget):
    """A custom widget that provides a foldable section."""
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        # The toggle button
        self.toggle_button = QToolButton(text=title, checkable=True, checked=True)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.toggle_button.setStyleSheet("QToolButton { border: none; text-align: left; font-size: 14px; }")
        self.toggle_button.toggled.connect(self.on_toggled)

        # The content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 0, 0, 0) # Indent children

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)

    def on_toggled(self, checked):
        """Updates the arrow and toggles visibility of the content area."""
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        self.content_area.setVisible(checked)

    def add_widget(self, widget):
        """Adds a widget to the collapsible content area."""
        self.content_layout.addWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App UI Schema")
        self.resize(800, 600)
        self.tab_counter = 1

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. Custom Tab Bar Area
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

        # 2. Content Area
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.add_new_tab(name="Tab 1")
        self.add_new_tab(name="Tab 2")
        self.add_new_tab(name="Tab 3")

        # 3. Bottom Button Bar
        bottom_layout = QHBoxLayout()
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")
        btn3 = QPushButton("Button 3")

        bottom_layout.addWidget(btn1)
        bottom_layout.addWidget(btn2)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn3)

        main_layout.addLayout(bottom_layout)

    def add_new_tab(self, checked=False, name=None):
        if not isinstance(name, str):
            name = f"Tab {self.tab_counter}"

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
            self,
            'Confirm Close',
            f"Are you sure you want to close {tab_name}?",
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

        for cat in range(1, 4):
            cat_box = CollapsibleBox(f"Category {cat}")
            cat_box.toggle_button.setStyleSheet("QToolButton { border: none; text-align: left; font-size: 16px; font-weight: bold; }")
            content_layout.addWidget(cat_box)

            for subcat in range(1, 3):
                subcat_box = CollapsibleBox(f"Subcategory {cat}.{subcat}")
                subcat_box.toggle_button.setStyleSheet("QToolButton { border: none; text-align: left; font-size: 14px; font-weight: bold; }")
                cat_box.add_widget(subcat_box)

                for row in range(1, 4):
                    row_frame = QFrame()
                    row_frame.setFrameShape(QFrame.Shape.Box)

                    row_layout = QHBoxLayout(row_frame)
                    row_layout.setContentsMargins(5, 5, 5, 5)
                    row_layout.addWidget(QLabel(f"Row {row}, with many fields"))

                    subcat_box.add_widget(row_frame)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        return scroll

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())