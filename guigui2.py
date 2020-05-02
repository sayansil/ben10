from __future__ import unicode_literals
import sys
import os
import numpy as np
import random
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style
style.use('seaborn-ticks')

progname = os.path.basename(sys.argv[0])
progversion = "0.1"




class MyCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyCanvas.__init__(self, *args, **kwargs)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1)
		

        self.languages = ["Java", "C++", "Cython", "Haskell", "Rust"]

        self.color = list()

        self.data = list()

        self.default_maxX = None
        self.default_maxY = None

        self.xmax = 0.1 #if (self.default_maxX == None) else self.default_maxX
        self.xmin = 0
        self.ymax = 0.1 #if (self.default_maxY == None) else self.default_maxY
        self.ymin = 0

		
        for j, lang in enumerate(self.languages):
            self.color.append('#' + ('%006x' % random.randrange(16**6)).upper())

            data_x, data_y = [], []

            self.data.append(np.row_stack((np.array(data_x), np.array(data_y))))

    def update_figure(self):
        self.data = list()

        self.xmax = 0.1 #if (self.default_maxX == None) else self.default_maxX
        self.xmin = 0
        self.ymax = 0.1 #if (self.default_maxY == None) else self.default_maxY
        self.ymin = 0
        
        for j, lang in enumerate(self.languages):

            data_x, data_y = [], []
            with open(lang + ".txt", "r") as file:
                line = file.readline()

                while(len(line) > 0):
                    point = [int(x) for x in line.split(',') if x.strip().isdigit()]
                    
                    if len(point) == 2:
                        data_x.append(point[0])
                        data_y.append(point[1])

                        #if self.default_maxX == None:
                        self.xmax = max([self.xmax, point[0]])
                        self.xmin = min([self.xmin, point[0]])

                        #if self.default_maxY == None:
                        self.ymax = max([self.ymax, point[1]])
                        self.ymin = min([self.ymin, point[1]])

                    line = file.readline()

            self.data.append(np.row_stack((np.array(data_x), np.array(data_y))))
                    

        
        self.axes.cla()
        self.axes.set_xlim(self.xmin, self.xmax)
        self.axes.set_ylim(self.ymin, self.ymax)
        self.axes.set_ylabel('Time (seconds)')
        self.axes.set_xlabel('Input Dimensions')

        for i, line in enumerate(self.data):
            self.axes.plot(line[0], line[1], self.color[i], label=self.languages[i])
            self.axes.legend(loc="upper right")

        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=10, height=4, dpi=100)

        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",)


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()