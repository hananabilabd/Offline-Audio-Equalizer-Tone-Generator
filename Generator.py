from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
import sys

from PyQt4 import QtGui
import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq

from IPython.display import Audio
import scipy.io.wavfile as wav
from scipy.io.wavfile import write



import pyglet
#import wavio


#from mainwindows import Ui_Dialog
Ui_Dialog, QDialog = loadUiType('generator.ui')

class main(QDialog, Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.falg = 0

        self.pushButton_2.clicked.connect(self.generate)
        self.pushButton.clicked.connect(self.file_save)
        #self.pushButton_3.clicked.connect(self.listen)

    def generate (self):
        f1= int(self.lineEdit.text())
        f2 =int( self.lineEdit_2.text())

        f3 = int(self.lineEdit_3.text())
        self.rate = int(self.lineEdit_4.text())
        self.flag =1


        def waveform(freq1, freq2, freq3, sec, sample_rate):
            time = np.linspace(0, sec, sample_rate * sec)
            signal1 = np.cos(2*freq1 * np.pi * time) + np.cos(2*freq2 * np.pi * time) + np.cos(2*freq3 * np.pi * time)
            #signal2 =  np.cos(2*freq2 * np.pi * time)
            #signal = signal1 + signal2
            #print(len(signal))
            return (signal, time)

        self.signal, time = waveform(freq1=f1, freq2=f2, freq3=f3, sec=3,sample_rate=self.rate)

        #sample_rate = 44100




        scaled = np.int16(self.signal/np.max(np.abs(self.signal)) * 32767)

        write('test.wav', 44100, scaled)


        music = pyglet.resource.media('test.wav')
        music.play()

        pyglet.app.run()





    def file_save(self):

        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', "C:\Users\Hanna Nabil\Documents", '*.wav')

        print(name)
        ff = str(name)

        scaled = np.int16(self.signal / np.max(np.abs(self.signal)) * 32767)

        wav.write(ff, self.rate, scaled)

        #T = 3  # sample duration (seconds)

        #t = np.linspace(0, T, T * self.rate, endpoint=False)
        #x = np.sin(2 * np.pi * f * t)
        #wavio.write(ff, x, self.rate, sampwidth=3)











app =QApplication(sys.argv)
window = main()
window.show ()
app.exec_()

