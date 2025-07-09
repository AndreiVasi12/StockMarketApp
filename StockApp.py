import yfinance as yf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
import sys


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class StockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Price Visualizer")
        self.setGeometry(200, 200, 1000, 700)

        # UI setup
        self.layout = QVBoxLayout()
        self.label = QLabel("Enter ticker symbol:")
        self.input_field = QLineEdit()
        self.interval_label = QLabel("Enter interval (e.g., 5m, 1h, 1d):")
        self.input_interval = QLineEdit()
        self.show_button = QPushButton("Show Data")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.interval_label)
        self.layout.addWidget(self.input_interval)
        self.layout.addWidget(self.show_button)

        # Placeholder for the matplotlib canvas
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        # Connect button
        self.show_button.clicked.connect(self.plot_data)

    def show_error_messagebox(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def plot_data(self):
        ticker = self.input_field.text().strip()
        interval = self.input_interval.text().strip()

        if not ticker or not interval:
            self.show_error_messagebox("Both fields must be filled in.")
            return

        try:
            df = yf.download(tickers=ticker, period='1d', interval=interval)
            if df.empty:
                self.show_error_messagebox("No data found. Check symbol or interval.")
                return

            self.canvas.axes.clear()
            self.canvas.axes.plot(df.index, df['Close'], label="Close Price")
            self.canvas.axes.set_title(f"{ticker.upper()} - Close Price")
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Price")
            self.canvas.axes.legend()
            self.canvas.draw()
        except Exception as e:
            self.show_error_messagebox(f"Error fetching data:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())
