import mutagen
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from main import *
import sys
import os
from pygame import mixer


class musicPlayer(QMainWindow):
     
     def __init__(self):
          super().__init__()
          self.ui = Ui_MainWindow()
          self.ui.setupUi(self)
          self.setWindowTitle('Music Player')
          self.setWindowIcon(QIcon('icons/main_icon.png'))
          self.screenSize = QDesktopWidget().screenGeometry()
          self.height = self.screenSize.height()
          self.width = self.screenSize.width()
          self.setFixedSize(int(self.width/3),int(self.height/3))
          self.ui.file_option.triggered.connect(self.openFile)
          self.ui.file_option.setShortcut("Ctrl+O")
          self.ui.exit_player.triggered.connect(lambda: exit())
          self.ui.exit_player.setShortcut("Ctrl+E")
          self.ui.action_play.triggered.connect(self.play_pause)
          self.ui.action_play.setShortcut("Ctrl+P")
          self.ui.action_pause.triggered.connect(self.play_pause)
          self.ui.action_pause.setShortcut("Ctrl+P")
          self.ui.action_stop.triggered.connect(self.play_pause)
          self.ui.action_stop.setShortcut("Ctrl+S")
          self.ui.volume.setMinimum(0)
          self.ui.volume.setMaximum(10)
          self.ui.volume.setValue(3)
          self.ui.volume.setSingleStep(1)
          self.ui.volume.valueChanged.connect(lambda vol: self.setVolume(vol))
          self.ui.progress.setMinimum(0)
          self.ui.progress.setValue(0)
          self.timer = QTimer()
          self.timer.timeout.connect(self.updateLabels)
          self.ui.volumeLabel.setText(f"Volume: {self.ui.volume.value()}")
          mixer.init()
          mixer.music.set_volume(0.3)
          self.ui.load.clicked.connect(self.openFile)
          self.ui.play_pause.clicked.connect(self.play_pause)
          self.ui.stop.clicked.connect(self.stopMusic)
          self.ui.clock.setPixmap(QPixmap('icons\clock.png').scaled(35,35))
          self.ui.tune.setPixmap(QPixmap('icons\music.png').scaled(25,25))
          self.ui.volume_icon.setPixmap(QPixmap('icons/volume_low.png').scaled(30,30))
          self.ui.progress_icon.setPixmap(QPixmap('icons/length.png').scaled(30,30))
          self.show()


     def stopMusic(self):
          mixer.music.stop()
          self.ui.progress.setValue(0)
          self.timer.stop()
          
     def play_pause(self):
          if self.play_pause == True:
               mixer.music.pause()
               self.timer.stop()
               self.play_pause = False
               self.ui.play_pause.setText(" Play")
               self.ui.play_pause.setIcon(QIcon('icons\play.png'))
          elif self.play_pause == False:
               mixer.music.unpause()
               self.timer.start(900)
               self.play_pause = True
               self.ui.play_pause.setText(" Pause")
               self.ui.play_pause.setIcon(QIcon('icons\pause.png'))
               

     def openFile(self):
          self.fname = QFileDialog.getOpenFileName(self,'Open File','Documents',"Audio File(*.mp3, *.ogg);;All Files (*.*)")
          if self.fname[0]=='':
               pass
          else:
               print((self.fname[0]))
               self.setFileAttributes()


     def setFileAttributes(self):
          self.audioFile = mutagen.File(self.fname[0])
          self.ui.title.setText(f" Track: {os.path.basename(self.fname[0])}")
          mixer.music.load(self.fname[0])
          mixer.music.play()
          self.timer.start(900)
          self.ui.progress.setMaximum(int(self.audioFile.info.length))
          self.total_duration_mins, self.total_duration_secs= divmod(int(self.audioFile.info.length),60)
          self.ui.play_pause.setIcon(QIcon('icons\pause.png'))
          self.ui.play_pause.setText(" Pause")
          self.play_pause = True


     def setVolume(self,vol):
          mixer.music.set_volume(vol/10)
          if vol == 0:
               self.ui.volume_icon.setPixmap(QPixmap('icons/mute.png').scaled(30,30))
          elif vol <4 and vol>0:
               self.ui.volume_icon.setPixmap(QPixmap('icons/volume_low.png').scaled(30,30))
          elif vol >=4 and vol<7:
               self.ui.volume_icon.setPixmap(QPixmap('icons/volume_medium.png').scaled(30,30))
          elif vol >=7:
               self.ui.volume_icon.setPixmap(QPixmap('icons/volume_high.png').scaled(30,30))
               
          self.ui.volumeLabel.setText("Volume:"+ str(self.ui.volume.value()))
          
          
     def updateLabels(self):
           minutes, seconds = divmod(int(mixer.music.get_pos()/1000.0),60)
           print(minutes,seconds)
           self.ui.duration.setText(f" Duration: {minutes:02d}:{seconds:02d} / {self.total_duration_mins}:{self.total_duration_secs} Min.")
           self.ui.progress.setValue((minutes+1)*seconds)
          
app = QApplication(sys.argv)
M = musicPlayer()
M.show()
sys.exit(app.exec_())
