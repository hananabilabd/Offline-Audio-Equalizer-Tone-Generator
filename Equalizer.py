from PyQt4.uic import loadUiType

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import pyglet
import scipy
from scipy.fftpack import rfft, irfft, fftfreq ,fft ,ifft

from scipy.io.wavfile import read
import scipy.io.wavfile as wav

Ui_MainWindow, QMainWindow = loadUiType('equalizer.ui')

import matplotlib.backends.backend_qt4agg
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

        self.pushButton_3.clicked.connect(self.browse_txt)
        self.pushButton.clicked.connect(self.browse)
        self.pushButton_2.clicked.connect(self.file_save)
        #self.pushButton_4.clicked.connect(self.hanna)

        self.figure = Figure()
        self.drawing = self.figure.add_subplot(111)

        self.drawing.plot()
        #self.drawing.plot.xlim(0, 1500)
        self.canvas = matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg(self.figure)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        self.addToolBar(self.toolbar)

        self.figure2 = Figure()
        self.drawing2 = self.figure2.add_subplot(111)
        self.drawing2.plot()
        self.canvas2 = matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg(self.figure2)
        self.mplvl.addWidget(self.canvas2)
        self.canvas2.draw()
        self.toolbar = NavigationToolbar(self.canvas2, self, coordinates=True)
        self.addToolBar(self.toolbar)

        self.figure3 = Figure()
        self.drawing3 = self.figure3.add_subplot(111)
        self.drawing3.plot()
        self.canvas3 = matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg(self.figure3)
        self.mplvl_2.addWidget(self.canvas3)
        self.canvas3.draw()
        self.toolbar = NavigationToolbar(self.canvas3, self, coordinates=True)
        self.addToolBar(self.toolbar)

        self.figure4 = Figure()
        self.drawing4 = self.figure4.add_subplot(111)
        self.drawing4.plot()
        self.canvas4 = matplotlib.backends.backend_qt4agg.FigureCanvasQTAgg(self.figure4)
        self.mplvl_2.addWidget(self.canvas4)
        self.canvas4.draw()
        self.toolbar = NavigationToolbar(self.canvas4, self, coordinates=True)
        self.addToolBar(self.toolbar)


        self.horizontalSlider.valueChanged.connect(self.valuechange)
        self.horizontalSlider_2.valueChanged.connect(self.valuechange2)
        self.horizontalSlider_3.valueChanged.connect(self.valuechange3)
        self.horizontalSlider_4.valueChanged.connect(self.valuechange4)
        self.horizontalSlider_5.valueChanged.connect(self.valuechange5)
        self.horizontalSlider_6.valueChanged.connect(self.valuechange6)
        self.horizontalSlider_7.valueChanged.connect(self.valuechange7)
        self.horizontalSlider_8.valueChanged.connect(self.valuechange8)
        self.horizontalSlider_9.valueChanged.connect(self.valuechange9)
        self.horizontalSlider_10.valueChanged.connect(self.valuechange10)


    def browse(self):

        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "C:\Users\Hanna Nabil\Documents",'*.wav')
        f= str(filepath)
        if f != "":
            spf = wave.open(f, 'r')



        import contextlib

        with contextlib.closing(wave.open(f, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            print "Duration is " , duration

        # Extract Raw Audio from Wav File
        self.signal = spf.readframes(-1)
        self.signal = np.fromstring(self.signal, 'Int16')
        self.fs = spf.getframerate()
        print "Sampling Rate is " ,self.fs

        # If Stereo
        if spf.getnchannels() == 2:
            print 'Just mono files'
            sys.exit(0)
        #print (self.signal[37990:38000])

        #self.time = np.linspace(0, len(self.signal) / fs, num=len(self.signal))
        self.time = np.linspace(0, duration, self.fs * duration)

        self.xfourier = fftfreq(self.signal.size, d=self.time[1] - self.time[0])

        self.yfourier = abs(fft(self.signal))
        #print len(self.time) ,len(self.xfourier) ,len(self.yfourier)

        self.zico = self.yfourier

        self.cut_signal = ifft(self.zico)

        self.drawOn1()
        self.drawOn3()

        #self.drawOn4()
        #self.drawOn2(self.zico)




    def valuechange (self ):
        z = str(self.horizontalSlider.value())
        self.label_11.setText(z+ 'dB')
        norm = float(z) / 30
        x1 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])

        yfourier1 = np.abs(fft(self.signal))
        # If our original signal time was in seconds, this is now in Hz
        #copy = self.yfourier[(self.x > 900)].copy()
        #self.zico = np.concatenate((self.yfourier[(self.x < 900)] * 0.3, self.yfourier[(self.x>900)]*0.3), axis=0)
        for i in x1:
            if x1[i] < 1000:
                self.zico[i] = norm * yfourier1[i]
        #self.zico =yfourier1

        self.cut_signal = ifft(self.zico)

        self.drawOn2()
        self.drawOn4()

    def valuechange2 (self ):
        z = str(self.horizontalSlider_2.value())
        self.label_12.setText(z+ 'dB')
        norm = float(z) / 30

        x2 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])

        yfourier2 = abs(fft(self.signal))
        # If our original signal time was in seconds, this is now in Hz
        for i in x2:
            if 1000 <x2[i] < 2000:
                self.zico[i] = norm * yfourier2[i]
        #self.zico =self.zico

        #self.zico = yfourier2

        self.cut_signal = ifft(self.zico)

        self.drawOn2()
        self.drawOn4()

    def valuechange3 (self ):
        z = str(self.horizontalSlider_3.value())
        self.label_13.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier3 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])

        yfourier3 = abs(fft(self.signal))
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier3:
            if 2000 <xfourier3[i] < 3000:
                self.zico[i] = norm * yfourier3[i]
        self.cut_signal = ifft(self.zico)
        self.drawOn2()
        self.drawOn4()
    def valuechange4 (self ):
        z = str(self.horizontalSlider_4.value())
        self.label_14.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier4 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier4 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier4:
            if 3000 <xfourier4[i] < 4000:
                self.zico[i] = norm * yfourier4[i]
        self.cut_signal = irfft(self.zico)
        self.drawOn2()
        self.drawOn4()
    def valuechange5 (self ):
        z = str(self.horizontalSlider_5.value())
        self.label_15.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier5 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier5 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier5:
            if 4000 <xfourier5[i] < 5000:
                self.zico[i] = norm * yfourier5[i]
        self.cut_signal = irfft(self.zico)
        self.drawOn2()
        self.drawOn4()
    def valuechange6 (self ):
        z = str(self.horizontalSlider_6.value())
        self.label_16.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier6 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier6 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier6:
            if 5000 < xfourier6[i] < 6000:
                self.zico[i] = norm * yfourier6[i]
        self.cut_signal = irfft(self.zico)

        self.drawOn2()
        self.drawOn4()
    def valuechange7 (self ):
        z = str(self.horizontalSlider_7.value())
        self.label_17.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier7 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier7 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier7:
            if 6000 < xfourier7[i] < 7000:
                self.zico[i] = norm * yfourier7[i]
        self.cut_signal = irfft(self.zico)
        self.drawOn2()
        self.drawOn4()

        self.drawOn2()
        self.drawOn4()
    def valuechange8 (self ):
        z = str(self.horizontalSlider_8.value())
        self.label_18.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier7 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier7 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier7:
            if 7000 < xfourier7[i] < 8000:
                self.zico[i] = norm * yfourier7[i]
        self.cut_signal = irfft(self.zico)

        self.drawOn2()
        self.drawOn4()
    def valuechange9 (self ):
        z = str(self.horizontalSlider_9.value())
        self.label_19.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier9 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier9 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier9:
            if 8000 < xfourier9[i] < 9000:
                self.zico[i] = norm * yfourier9[i]
        self.cut_signal = irfft(self.zico)

        self.drawOn2()
        self.drawOn4()
    def valuechange10 (self ):
        z = str(self.horizontalSlider_10.value())
        self.label_20.setText(z+ 'dB')
        norm = float(z) / 30
        xfourier10 = fftfreq(self.signal.size, d=self.time[1] - self.time[0])
        yfourier10 = rfft(self.signal)
        # If our original signal time was in seconds, this is now in Hz
        for i in xfourier10:
            if 9000 < xfourier10[i] < 10000:
                self.zico[i] = norm * yfourier10[i]
        self.cut_signal = irfft(self.zico)

        self.drawOn2()
        self.drawOn4()





    def file_save(self):

        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', "C:\Users\Hanna Nabil\Documents", '*.wav')

        print "Your wave file saved successfully in ",name
        f = str(name)
        import scipy.io.wavfile as wav
        wav.write(f, 44100, self.cut_signal)

    def browse_txt(self):

        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "C:\Users\Hanna Nabil\Desktop", '*.txt')


        with open(filepath, "r") as f:
            content = f.readlines()
        content = [s.strip() for s in content]
        print len(content)
        p=[]
        index = 0

        while index < len(content):

            y = float(content[index])

            p.append(y)

            index += 1
        self.signal = np.array(p)

        self.time = np.linspace(0, 1, 38000 * 1)

        freq = fftfreq(self.signal.size, 1.0 / 38000)
        self.xfourier = freq[:int(len(freq) / 2)]

        mag = abs(fft(self.signal))
        self.yfourier = mag[:int(len(mag) / 2)]

        self.zico = self.yfourier

        self.cut_signal = ifft(self.zico)

        self.drawOn1()
        self.drawOn3()
    '''
    def browse_txt(self):

        filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "C:\Users\Hanna Nabil\Desktop",'*.txt')

        y=[0.0,0.0,0.0,0.0,0.0,0.0]
        x=[0.0,0.0,0.0,0.0,0.0,0.0]
        with open(filepath, "r") as f:
            content = f.readlines()
        content = [s.strip() for s in content]
        print len(content)


        index = 0
        p0=0
        p=[]
        while index < len(content):
            x[0] = x[1]
            x[1] = x[2]
            x[2] = x[3]
            x[3] = x[4]
            x[4] = x[5]
            x[5] = float(content[index])
            y[0] = y[1]
            y[1] = y[2]
            y[2] = y[3]
            y[3] = y[4]
            y[4] = y[5]
            #x = float(content[index])
            y[5] =0.00002* x[5] + 0.00010* x[4] +0.00020* x[3] + 0.00020 * x[2] +0.00010 * x[1] +0.00002 * x[0]
            - ( -4.19797796)*y [4]-  7.10418975*y[3] -(-6.05213597 )*y[2] -2.59358135   *y[1]- ( -0.44701336)*y[0]
            #p0 = float(content[index])
            p.append(y[5])


            index += 1
        self.signal=np.array(p)


        self.time = np.linspace(0, 1, 38000 * 1)


        freq = fftfreq(self.signal.size, 1.0/38000)
        self.xfourier =freq[:int(len(freq) / 2)]

        mag= abs(fft(self.signal))
        self.yfourier = mag[:int(len(mag) / 2)]

        self.zico = self.yfourier

        self.cut_signal = ifft(self.zico)

        self.drawOn1()
        self.drawOn3()

        
    def hanna(self):
        from math import sin, pi


        x = [0] * 38000

        for i in range(38000):
            x[i] = sin(2 * pi * 10000 * i / 38000)   + sin(2 * pi * 7000 * i / 38000)
        #x=np.cos(500 * np.pi * 1) + np.cos(1500 * np.pi * 1)

        p0=0
        p=[]

        y = [0] * 38000
        for n in range(6, len(x)):
            #y[n] =0.00159499* x[n] + 0.00797494* x[n-1] +0.01594988* x[n-2] + 0.01594988 * x[n-3] +0.00797494 * x[n-4] +0.00159499 * x[n-5]- ( -2.86973768)*y [n-1]- 3.5795904*y[n-2] -(-2.34473216 )*y[n-3] -0.79780141   *y[n-4]- ( -0.11188235)*y[n-5] #lowpass fc =4k
            #y[n] =0.334492* x[n] -1.67246* x[n-1] +3.34492* x[n-2] -3.34492 * x[n-3] +1.67246 * x[n-4] -0.334492 * x[n-5]- ( -2.86973768)*y [n-1]- 3.5795904*y[n-2] -(-2.34473216 )*y[n-3] -0.79780141  *y[n-4]- ( -0.11188235)*y[n-5] #highpass fc =4k
            ##y[n] = 0.0101 * x[n] - 0.0202 * x[n - 2] + 0.0101 * x[n - 4] + 2.4354 * y[n - 1] - 3.1869 * y[n - 2] + 2.0889 * y[n - 3] - 0.7368 * y[n - 4] #6KHz->8Khz Bandpass Filter
            y[n] = 0.00334 * x[n] -0.01002 * x[n - 2] + 0.01002 * x[n - 4] -0.00334*x[n-6]+2.17580946  * y[n - 1] - 3.92807914 * y[n - 2] + 3.82844176 * y[n - 3] -3.1510065 * y[n - 4] +1.39512727 *y[n-5]- 0.51424268*y[n-6] # 6KHz->8Khz Bandpass Filter of order 3
            #p.append(y[5])



        self.signal=np.array(x)
        self.zico =np.array(y)


        self.time = np.linspace(0, 1, 38000 * 1)


        freq = fftfreq(self.signal.size, 1.0/38000)
        self.xfourier =freq[:int(len(freq) / 2)]

        mag= abs(fft(self.signal))
        self.yfourier = mag[:int(len(mag) / 2)]



        mag = abs(fft(self.zico))
        self.zico = mag[:int(len(mag) / 2)]

        #self.zico = self.yfourier

        self.cut_signal = ifft(self.zico)

        self.drawOn1()
        self.drawOn2()
        self.drawOn3()

        '''
    #plot fourier before manipulation
    def drawOn1(self):
        #self.drawing.hold(False)
        self.drawing.clear()
        # put the values to draw
        self.drawing.plot(self.xfourier,self.yfourier)
        self.drawing.set_xlim([0,18000])
        #self.drawing.set_ylim([0, 1000000])

        self.canvas.draw()
    #plot fourier after mainpulation
    def drawOn2(self):
        #self.drawing2.hold(False)
        self.drawing2.clear()
        self.drawing2.plot(self.xfourier ,self.zico)
        self.drawing2.set_xlim([0, 18000])
        #self.drawing2.set_ylim([0, 100000])
        self.canvas2.draw()

    #plot time domain before manipulation
    def drawOn3(self):
        #self.drawing3.hold(False)
        self.drawing3.clear()
        # put the values to draw
        self.drawing3.plot(self.time,self.signal)
        self.drawing3.set_xlim([0, 0.001])
        self.canvas3.draw()
    #plot time domain after manipulation
    def drawOn4(self):
        #self.drawing4.hold(False)
        self.drawing4.clear()
        # put the values to draw
        self.drawing4.plot(self.time,self.cut_signal)
        self.drawing4.set_xlim([0, 0.001])
        self.canvas4.draw()



if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import numpy as np

    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

