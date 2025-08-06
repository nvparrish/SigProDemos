import pyaudio
import wave
import numpy as np
import locked_buffer
from multiprocessing import Lock
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AudioStream:
    ''' Class to manage an audio stream.
    
        In order for this to work, you need to make sure your sound device is properly configbured.
        `arecord --list-devices` This command will list the devices on the system. They will be
                                enumerated by card number and subdevice counts.
        Once the device has been identified and selected, you can configure the value by going to
        /etc/modprobe.d/alsa-base.conf.  Then set the snd-card-usb-caiaq index=<card id>
        where the card id is the number correspdonding to the desired device.

    '''
    def __init__(self):
        self.p = pyaudio.PyAudio()

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')) > 0:
                print('Input Device id ', i, ' - ', self.p.get_device_info_by_host_api_device_index(0,i).get('name'))

        device_index = int(input('Enter your device choice: '))

        #self.CHUNK = 4096
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.DEVICE_INDEX = device_index
        self.CHANNELS = 1
        self.RATE = 48000
        self.RECORD_SECONDS = 5
        self.FFT_BIN = 1024
        self.dataMutex = Lock()
        with self.dataMutex:
            self.isActive = False
            self.fft_amp = None


    def __del__(self):
        self.p.terminate()

    def activate(self):
        logger.warning("Opening stream:")
        self.stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             input_device_index=self.DEVICE_INDEX,
                             frames_per_buffer=self.CHUNK)

        logger.warning("Activating")
        with self.dataMutex:
            self.isActive = True
            logger.warning("Activation setting: %r", self.isActive)
        #for i in range(0, int(self.RATE/self.CHUNK * self.RECORD_SECONDS)):

    def read_data(self):
        with self.dataMutex:
            if self.isActive:
                logger.debug("Active, doing stuff ...")
                data = self.stream.read(self.CHUNK, exception_on_overflow = False) # Avoid exception on overflow for now
                buffer = np.frombuffer(data, np.int16)
                logger.debug(buffer)
                self.fft_amp = np.log(np.abs(np.fft.rfft(buffer, n=self.FFT_BIN))+1e-3)
                self.frequencies = np.fft.rfftfreq(self.FFT_BIN, 1/self.RATE)
                #self.fft_amp = np.abs(np.fft.fft(buffer))
                logger.debug(self.fft_amp)

    def deactivate(self):
        with self.dataMutex:
            self.isActive = False
        self.stream.close()

if __name__ == "__main__":
    stream = AudioStream()
    stream.activate()
