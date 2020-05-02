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
		

        self.lnum = 5
        #self.num = [50]*self.lnum
        self.num = [50, 100, 150, 200, 250]

        self.xindex = [1]*self.lnum
        self.color = list()

        self.data = list()

        self.xmax, self.xmin = 0, 0
        self.ymax, self.ymin = 0, 0

        self.legends = list()
		
        for j in range(self.lnum):
            self.color.append('#' + ('%006x' % random.randrange(16**6)).upper())
            self.legends.append("execution " + str(j+1))

            data_x, data_y = [None]*self.num[j], [None]*self.num[j]
            for i in range(self.num[j]):
                #data_x[i] = float(input())
                data_x[i] = i * 10
                self.xmax = max([self.xmax, data_x[i]])
                self.xmin = min([self.xmin, data_x[i]])

            for i in range(self.num[j]):
                #data_y[i] = float(input())
                data_y[i] = np.power(i, j*0.25 + 1)
                self.ymax = max([self.ymax, data_y[i]])
                self.ymin = min([self.ymin, data_y[i]])

            self.data.append(np.row_stack((np.array(data_x), np.array(data_y))))

    def update_figure(self):
        '''
        #self.num = [50]*self.lnum
        self.num = [50, 100, 150, 200, 250]

        self.color = list()

        self.data = list()

        self.xmax, self.xmin = 0, 0
        self.ymax, self.ymin = 0, 0

        self.legends = list()
        
        for j in range(self.lnum):
            self.color.append('#' + ('%006x' % random.randrange(16**6)).upper())
            self.legends.append("execution " + str(j+1))

            data_x, data_y = [None]*self.num[j], [None]*self.num[j]
            for i in range(self.num[j]):
                #data_x[i] = float(input())
                data_x[i] = i * 10
                self.xmax = max([self.xmax, data_x[i]])
                self.xmin = min([self.xmin, data_x[i]])

            for i in range(self.num[j]):
                #data_y[i] = float(input())
                data_y[i] = np.power(i, j*0.25 + 1)
                self.ymax = max([self.ymax, data_y[i]])
                self.ymin = min([self.ymin, data_y[i]])

            self.data.append(np.row_stack((np.array(data_x), np.array(data_y))))

        '''
        self.axes.cla()
        self.axes.set_xlim(self.xmin, self.xmax)
        self.axes.set_ylim(self.ymin, self.ymax)
        self.axes.set_ylabel('Time (seconds)')
        self.axes.set_xlabel('Input Dimensions')
        for i, line in enumerate(self.data):
            self.axes.plot(line[0][0:self.xindex[i]], line[1][0:self.xindex[i]], self.color[i])

            if self.xindex[i] < line.shape[1]:
                self.xindex[i] = self.xindex[i] + 1


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