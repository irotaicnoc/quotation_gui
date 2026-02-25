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
        self.tabs.addTab(self.create_tab_content(), "Tab 1")
        self.tabs.addTab(QWidget(), "Tab 2")
        self.tabs.addTab(QWidget(), "Tab 3")
        self.tabs.addTab(QWidget(), "+")  # The add tab button
        main_layout.addWidget(self.tabs)

        # 2. Bottom Button Bar
        bottom_layout = QHBoxLayout()
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")
        btn3 = QPushButton("Button 3")

        bottom_layout.addWidget(btn1)
        bottom_layout.addWidget(btn2)
        bottom_layout.addStretch()  # Pushes Button 3 to the far right
        bottom_layout.addWidget(btn3)

        main_layout.addLayout(bottom_layout)

    @staticmethod
    def create_tab_content():
        """Creates the scrollable area containing categories and rows."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Generate Mock Categories and Rows
        for cat in range(1, 4):  # Example: 3 Categories
            cat_label = QLabel(f"<br><b>Category {cat}</b>")
            content_layout.addWidget(cat_label)

            for row in range(1, 6):  # Example: 5 Rows per category
                row_frame = QFrame()
                row_frame.setFrameShape(QFrame.Shape.Box)  # Creates the box outline

                row_layout = QHBoxLayout(row_frame)
                row_layout.setContentsMargins(5, 5, 5, 5)
                row_layout.addWidget(QLabel(f"Row {row}, with many fields"))

                content_layout.addWidget(row_frame)

        content_layout.addStretch()  # Pushes all content to the top
        scroll.setWidget(content_widget)
        return scroll


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
