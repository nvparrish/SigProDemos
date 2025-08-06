import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore
import numpy as np
import random
import audio_stream
import logging
import math

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live plot")

        # FFT amplitude plot
        self.plot = pg.plot()

        self.stream = audio_stream.AudioStream()
        self.stream.activate()
        self.stream.read_data()
        self.t = np.arange(self.stream.FFT_BIN)
        # self.freq = np.fft.fftfreq(self.t.shape[-1])
        # self.magnitude_spectrum = np.abs(np.fft.rfft(self.t))
        # self.frequencies = np.fft.rfftfreq(self.t.shape[0], 1/self.stream.RATE)

        self.setCentralWidget(self.plot)
        # self.time = list(range(10)) # [1,2,3,4,5,6,7,8,9,10]
        #self.temperature = [random.randint(20,40) for _ in range(10)] #[30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        #self.bargraph = pg.BarGraphItem(x=self.time, y0=[0]*10, y1=self.temperature, height=self.temperature, width=1)
        logger.debug("Frequencies:", self.stream.frequencies)
        # self.bargraph = pg.BarGraphItem(x=self.freq[self.freq >= 0], y0=[0]*(self.stream.FFT_BIN//2), y1=self.stream.fft_amp[self.freq >= 0], height=self.stream.fft_amp[self.freq >= 0], width=abs(self.freq[0]-self.freq[1]))
        # self.bargraph = pg.BarGraphItem(x=np.log(self.stream.frequencies), y=[0]*(self.stream.fft_amp.shape[0]), y1=self.stream.fft_amp, height=self.stream.fft_amp, width=np.log(abs(self.stream.frequencies[0]-self.stream.frequencies[1])))
        #self.plot.setXRange(np.min(self.freq), np.max(self.freq),padding=0)
        #self.plot.setXRange(0, np.max(self.stream.frequencies),padding=0)
        # Max possible is A*N/2
        #self.plot.setYRange(0,np.log(2**10*self.stream.FFT_BIN/2+1),padding=0)
        # self.plot.addItem(self.bargraph)
        self.line = self.plot.plot(self.stream.frequencies, y=self.stream.fft_amp)
        self.plot.setLogMode(x=True, y=False)   # Set the axis markings to log scale
        self.plot.setXRange(np.log(10), np.log10(self.stream.frequencies[-1]))
        self.plot.setYRange(-2, np.log(2**12*self.stream.FFT_BIN/2+1),padding=0, update=False)

        # Add a timer to get new entries
        self.timer = QtCore.QTimer()
        interval = (self.stream.FFT_BIN / self.stream.RATE) * 1000
        logger.debug("Interval is:", interval, "ms")
        self.timer.setInterval(100) # Interval at number of milliseconds, 85.333 ms/buffer
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        #self.time = self.time[1:]
        #self.time.append(self.time[-1]+1)
        #self.temperature = self.temperature[1:]
        #self.temperature.append(random.randint(20,40))
        #help(self.bargraph.setData)
        #self.bargraph.setOpts(x = self.time, y0 = [0]*10, y1 = self.temperature, height = self.temperature)
        logger.debug("Updating plot")
        self.stream.read_data()
        #self.bargraph.setOpts(x = self.freq[self.freq >= 0], y0=[0]*(self.stream.FFT_BIN//2), y1=self.stream.fft_amp[self.freq >= 0], height=self.stream.fft_amp[self.freq >= 0])
        # self.bargraph.setOpts(x=np.log(self.stream.frequencies), y=[0]*(self.stream.fft_amp.shape[0]), y1=self.stream.fft_amp, height=self.stream.fft_amp, width=np.log(abs(self.stream.frequencies[0]-self.stream.frequencies[1])))
        self.line.setData(x=self.stream.frequencies, y=self.stream.fft_amp)
        self.plot.setLogMode(x=True, y=False)   # Set the axis markings to log scale
        logger.info(np.log(self.stream.frequencies[-1]))
        self.plot.setXRange(np.log(10), np.log10(self.stream.frequencies[-1]))
        self.plot.setYRange(-2, np.log(2**12*self.stream.FFT_BIN/2+1),padding=0, update=False)



if __name__ == "__main__":
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logger.info('Started')
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec()
