import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

DB_FILE = 'parking_data.db'

class DataViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Data Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Spot", "Status", "Timestamp"])
        self.table.horizontalHeader().setStretchLastSection(True)

        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.load_data)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT spot, status, timestamp FROM parking_log ORDER BY timestamp DESC")
            for row_idx, row_data in enumerate(c.fetchall()):
                self.table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                    self.table.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())
