import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore
import random

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live plot")

        # Temperature verses time plot
        self.plot = pg.plot()
        self.setCentralWidget(self.plot)
        self.time = list(range(10)) # [1,2,3,4,5,6,7,8,9,10]
        self.temperature = [random.randint(20,40) for _ in range(10)] #[30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.bargraph = pg.BarGraphItem(x=self.time, y0=[0]*10, y1=self.temperature, height=self.temperature, width=1)
        #self.plot.setXRange(0,256,padding=0)
        self.plot.setYRange(0,256,padding=0)
        self.plot.addItem(self.bargraph)

        # Add a timer to simuate new temperature measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1]+1)
        self.temperature = self.temperature[1:]
        self.temperature.append(random.randint(20,40))
        #help(self.bargraph.setData)
        self.bargraph.setOpts(x = self.time, y0 = [0]*10, y1 = self.temperature, height = self.temperature)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec()

