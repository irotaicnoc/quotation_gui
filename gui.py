import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QPushButton, QScrollArea,
                             QLabel, QFrame)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App UI Schema")
        self.resize(800, 600)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. Tab Widget
        self.tabs = QTabWidget()
        # All tabs now share the same structure
        self.tabs.addTab(self.create_tab_content(), "Tab 1")
        self.tabs.addTab(self.create_tab_content(), "Tab 2")
        self.tabs.addTab(self.create_tab_content(), "Tab 3")
        self.tabs.addTab(QWidget(), "+") # The add tab button
        main_layout.addWidget(self.tabs)

        # 2. Bottom Button Bar
        bottom_layout = QHBoxLayout()
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")
        btn3 = QPushButton("Button 3")

        bottom_layout.addWidget(btn1)
        bottom_layout.addWidget(btn2)
        bottom_layout.addStretch() # Pushes Button 3 to the far right
        bottom_layout.addWidget(btn3)

        main_layout.addLayout(bottom_layout)

    def create_tab_content(self):
        """Creates the scrollable area containing categories, subcategories, and rows."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Generate Hierarchy: Categories -> Subcategories -> Rows
        for cat in range(1, 4): # Example: 3 Categories
            cat_label = QLabel(f"<h2>Category {cat}</h2>")
            content_layout.addWidget(cat_label)

            for subcat in range(1, 3): # Example: 2 Subcategories per category
                subcat_label = QLabel(f"<b>Subcategory {cat}.{subcat}</b>")
                subcat_label.setContentsMargins(20, 10, 0, 5) # Indented
                content_layout.addWidget(subcat_label)

                for row in range(1, 4): # Example: 3 Rows per subcategory
                    row_frame = QFrame()
                    row_frame.setFrameShape(QFrame.Shape.Box) # Creates the box outline

                    row_layout = QHBoxLayout(row_frame)
                    row_layout.setContentsMargins(5, 5, 5, 5)

                    row_label = QLabel(f"Row {row}, with many fields")
                    row_label.setContentsMargins(40, 0, 0, 0) # Indent the row text slightly
                    row_layout.addWidget(row_label)

                    content_layout.addWidget(row_frame)

        content_layout.addStretch() # Pushes all content to the top
        scroll.setWidget(content_widget)
        return scroll

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())