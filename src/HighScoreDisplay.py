# high_score_display.py
import sys

from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout,
                             QWidget)


class HighScoreDisplay(QWidget):
    def __init__(self, high_scores):
        super().__init__()
        
        self.setWindowTitle("High Scores")
        
        # Layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Top 10 High Scores")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # High score labels
        for i, score in enumerate(high_scores, start=1):
            score_label = QLabel(f"{i}. {score}")
            score_label.setStyleSheet("font-size: 16px;")
            layout.addWidget(score_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        # Set the layout
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 300)

def display_high_scores(high_scores):
    app = QApplication(sys.argv)
    window = HighScoreDisplay(high_scores)
    window.show()