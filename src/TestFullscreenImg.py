from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal
import sys
import time
import threading

class myImageDisplayApp (QObject):

    # Define the custom signal
    # https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#the-pyqtslot-decorator
    signal_update_image = pyqtSignal(str)

    def __init__ (self):

        super().__init__()

        # Setup the seperate thread 
        # https://stackoverflow.com/a/37694109/4988010
        self.thread = threading.Thread(target=self.run_img_widget_in_background) 
        self.thread.daemon = True
        self.thread.start()

    def run_img_widget_in_background(self):
        self.app = QApplication(sys.argv)
        self.my_bg_qt_app = qtAppWidget(main_thread_object=self)
        self.app.exec_()

    def emit_image_update(self, pattern_file=None):
        print('emit_image_update signal')
        self.signal_update_image.emit(pattern_file)


class qtAppWidget (QLabel):

    def __init__ (self, main_thread_object):

        super().__init__()

        # Connect the singal to slot
        main_thread_object.signal_update_image.connect(self.updateImage)

        self.setupGUI()

    def setupGUI(self):

        self.app = QApplication.instance()

        # Get avaliable screens/monitors
        # https://doc.qt.io/qt-5/qscreen.html
        # Get info on selected screen 
        self.selected_screen = 0            # Select the desired monitor/screen

        self.screens_available = self.app.screens()
        self.screen = self.screens_available[self.selected_screen]
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()

        # Create a black image for init 
        self.pixmap = QPixmap(self.screen_width, self.screen_height)
        self.pixmap.fill(QColor('black'))

        # Create QLabel object
        self.img_widget = QLabel()

        # Varioius flags that can be applied to make displayed window frameless, fullscreen, etc...
        # https://doc.qt.io/qt-5/qt.html#WindowType-enum
        # https://doc.qt.io/qt-5/qt.html#WidgetAttribute-enum
        self.img_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint)
        
        # Hide mouse cursor 
        self.img_widget.setCursor(Qt.BlankCursor)       

        self.img_widget.setStyleSheet("background-color: black;") 

        self.img_widget.setGeometry(0, 0, self.screen_width, self.screen_height)            # Set the size of Qlabel to size of the screen
        self.img_widget.setWindowTitle('myImageDisplayApp')
        self.img_widget.setAlignment(Qt.AlignCenter | Qt.AlignTop) #https://doc.qt.io/qt-5/qt.html#AlignmentFlag-enum                         
        self.img_widget.setPixmap(self.pixmap)
        self.img_widget.show()

        # Set the screen on which widget is on
        self.img_widget.windowHandle().setScreen(self.screen)
        # Make full screen 
        self.img_widget.showFullScreen()
        

    def updateImage(self, pattern_file=None):
        print('Pattern file given: ', pattern_file)
        self.img_widget.clear()                     # Clear all existing content of the QLabel
        
        self.pixmap.fill(QColor('green'))
        pixmap = QPixmap(pattern_file).scaled(self.screen_width,self.screen_height, Qt.KeepAspectRatio)         # Update pixmap with desired image
        self.pixmap = pixmap

        self.img_widget.setPixmap(self.pixmap)      # Show desired image on Qlabel

if __name__ == "__main__":

    myapp = myImageDisplayApp()

    print('Update the displayed image in the QT app running in background')
    myapp.emit_image_update('elefant.jpg')
    time.sleep(2)