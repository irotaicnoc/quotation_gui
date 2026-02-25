import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QScrollArea,
                             QLabel, QFrame, QMessageBox, QToolButton,
                             QTabBar, QStackedWidget)

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

        # Standalone button placed immediately after the tabs
        self.add_btn = QToolButton()
        self.add_btn.setText("+")
        self.add_btn.clicked.connect(self.add_new_tab)

        tab_layout.addWidget(self.tab_bar)
        tab_layout.addWidget(self.add_btn)
        tab_layout.addStretch() # Pushes the tabs and button to the left

        main_layout.addLayout(tab_layout)

        # 2. Content Area (Linked to the custom tab bar)
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Initialize default tabs
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
        """Switches the visible content when a tab is clicked."""
        if index >= 0:
            self.stack.setCurrentIndex(index)

    def close_tab(self, index):
        """Handles the close request, removing the tab and its content."""
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
            cat_label = QLabel(f"<h2>Category {cat}</h2>")
            content_layout.addWidget(cat_label)

            for subcat in range(1, 3):
                subcat_label = QLabel(f"<b>Subcategory {cat}.{subcat}</b>")
                subcat_label.setContentsMargins(20, 10, 0, 5)
                content_layout.addWidget(subcat_label)

                for row in range(1, 4):
                    row_frame = QFrame()
                    row_frame.setFrameShape(QFrame.Shape.Box)

                    row_layout = QHBoxLayout(row_frame)
                    row_layout.setContentsMargins(5, 5, 5, 5)

                    row_label = QLabel(f"Row {row}, with many fields")
                    row_label.setContentsMargins(40, 0, 0, 0)
                    row_layout.addWidget(row_label)

                    content_layout.addWidget(row_frame)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        return scroll

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())