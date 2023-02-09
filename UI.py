# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.axes_grid1 import make_axes_locatable

from numpy import *
from init import * #own module


class GraphPlotWindow(QMainWindow):

    def __init__(self):
        
        super().__init__()

        uic.loadUi("UI.ui", self)
        
        self.setWindowTitle("CNN fit visualisation tool")
        self.radioButton_MD.setChecked(True)
        self.button_exit.clicked.connect(self.on_exit)
        self.fit_button.clicked.connect(self.on_plot)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)        
        self.main_widget.layout().addWidget(self.canvas)
        self.get_input_values()
        self.update_plot()
        self.set_init_controls()
        
    def set_init_controls(self):
        self.radioButton_MD.setChecked(True)

    def get_input_values(self):

        if self.radioButton_MD.isChecked():
            self.contrast ='MD'
        elif self.radioButton_FA2D.isChecked():
            self.contrast ='FAIP'
            
        self.sample = self.sample_lineEdit.text()
       
    def update_plot(self):
        self.get_input_values()
        
        self.figure.clear()
        ax_1=self.figure.add_subplot(141)
        ax_2=self.figure.add_subplot(142)
        ax_3=self.figure.add_subplot(143)
        ax_4=self.figure.add_subplot(144)
        
        ax_1.scatter(eval(f"sample{self.sample}.ts_meas_{self.contrast}")\
                     ,eval(f"sample{self.sample}.ts_pred_{self.contrast}"))
        test_R2 = eval(f"sample{self.sample}.test_R2_{self.contrast}")
        ax_1.set_title(f"Scatter plot, $R^2={test_R2:.2f}$")
        lims, dif_lims  = eval(f"sample{self.sample}.get_lims('{self.contrast}','{self.sample}')")
        ax_1.plot([0, lims[1]], [0, lims[1]], 'r')
        ax_1.set_xlim(lims[0],lims[1])
        ax_1.set_ylim(lims[0],lims[1])
        ax_1.set_xlabel("Measured")
        ax_1.set_ylabel("Predicted")
        ax_1.set_aspect('equal', 'box')
        
        img = ax_2.imshow(eval(f"sample{self.sample}.I_meas_{self.contrast}"), cmap = "gray")
        ax_2.set_title(f"{self.contrast} measured")
        ax_2.axis("off")
        img.set_clim(lims[0],lims[1])
        
        divider = make_axes_locatable(ax_2)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        self.figure.colorbar(img, cax=cax, orientation='vertical', fraction=0.046)

        img = ax_3.imshow(eval(f"sample{self.sample}.I_pred_{self.contrast}"), cmap = "gray")
        ax_3.set_title(f"{self.contrast} predicted")
        ax_3.axis("off")
        img.set_clim(lims[0],lims[1])
        divider = make_axes_locatable(ax_3)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        self.figure.colorbar(img, cax=cax, orientation='vertical', fraction=0.046)        

        cdict = {'red':   ((0.0, 0.0, 0.0),
                           (0.5, 0.0, 0.0),
                           (1.0, 1.0, 1.0)),
                 'blue':  ((0.0, 0.0, 0.0),
                           (1.0, 0.0, 0.0)),
                 'green': ((0.0, 0.0, 1.0),
                           (0.5, 0.0, 0.0),
                           (1.0, 0.0, 0.0))}
        
        cmap = mcolors.LinearSegmentedColormap('my_colormap', cdict, 100)
        cmap.set_over('w')
        
        img = ax_4.imshow(eval(f"sample{self.sample}.I_diff_{self.contrast}"), cmap = cmap)
        ax_4.set_title(f"Difference")
        ax_4.axis("off")
        img.set_clim(dif_lims[0],dif_lims[1])
        divider = make_axes_locatable(ax_4)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        self.figure.colorbar(img, cax=cax, orientation='vertical', fraction=0.046)  
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        self.figure.canvas.update()
        
    def on_plot(self):
        self.update_plot()

    def on_exit(self):
        self.close()


if __name__ == '__main__':

    font = QFont()
    font.setPointSize(10)

    application = QApplication(sys.argv)
    application.setFont(font)

    window = GraphPlotWindow()
    window.show()

    sys.exit(application.exec_())
