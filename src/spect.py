#!/usr/bin/env python

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import pyaudio
import struct
import sys

# defs
FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 2**11




def specGraph(rate):

    app = QtGui.QApplication([])
    app.quitOnLastWindowClosed()

    # create window
    mainWindow = QtGui.QMainWindow()
    mainWindow.setWindowTitle("Live Spectrogram")  # Title
    mainWindow.resize(800, 300)  # Size

    # create widget
    wid = QtGui.QWidget()
    mainWindow.setCentralWidget(wid)

    # create layout
    lay = QtGui.QVBoxLayout()
    wid.setLayout(lay)

    pwid = pg.PlotWidget(name="spectrogram")
    p = pwid.getPlotItem()
    p.setXRange(0,CHUNK*2)

    p.setLogMode(y=True)
    lay.addWidget(pwid)
    mainWindow.show()
    pa = pyaudio.PyAudio()
    stream = open_mic_stream(rate, pa)

    while 1:
        update(app, p, stream)

def find_input_device(pa):
    device_index = None
    for i in range(pa.get_device_count()):
        devinfo = pa.get_device_info_by_index(i)
        print("Device %d: %s" % (i, devinfo["name"]))

        for keyword in ["mic", "input"]:
            if keyword in devinfo["name"].lower():
                print("Found an input: device %d - %s" % (i, devinfo["name"]))
                device_index = i
                return device_index

    if device_index == None:
        print("No preferred input found; using default input device.")

    return device_index

def open_mic_stream(rate, pa):
    device_index = find_input_device(pa)

    stream = pa.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=rate,
                          input=True,
                          input_device_index=device_index,
                          frames_per_buffer=CHUNK)

    return stream

def listen(stream):
    block = stream.read(CHUNK)
    return np.fromstring(block, np.int16)


def update(app, p, stream):
    test = listen(stream)
    p.clear()
    p.plot(abs(np.fft.fftshift(np.fft.fft(test))))
    QtGui.QApplication.processEvents()


if __name__ == "__main__" :
    rate = int(sys.argv[1])
    specGraph(rate)
