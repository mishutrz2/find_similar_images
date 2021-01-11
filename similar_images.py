from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
from PyQt5.QtGui import QPixmap, QImage

import matplotlib.pyplot as plt
import numpy as np
from skimage import color
from skimage.feature import local_binary_pattern

import sys
import os

from calc_hist_set import calc_set



#	select image from resources/img folder
#	-histogram set calculation-
#	show image + the most similar 3 images


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Similar"
        self.setStyleSheet("background-color: gray;")
        self.top = 200
        self.left = 30
        self.width = 250
        self.height = 100
        self.InitWindow()


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("iconita.png"))
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(200,50)
        hbox = QHBoxLayout()
        hbox_buttons = QHBoxLayout()
        vbox = QVBoxLayout()

        #labels
        self.label = QLabel()
        hbox.addWidget(self.label)
        self.labelImage1 = QLabel()
        hbox.addWidget(self.labelImage1)
        self.labelImage2 = QLabel()
        hbox.addWidget(self.labelImage2)
        self.labelImage3 = QLabel()
        hbox.addWidget(self.labelImage3)

        #buttons
        self.btn1 = QPushButton("Open Image")
        self.btn1.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        self.btn1.setFixedSize(QtCore.QSize(200, 30))
        self.btn1.setStyleSheet("background-color: green; color: white; font: bold 14px;")
        self.btn_search = QPushButton("Search")
        self.btn_search.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        self.btn_search.setFixedSize(QtCore.QSize(200, 30))
        self.btn_search.setStyleSheet("background-color: green; color: white; font: bold 14px;")
        self.btn1.clicked.connect(self.getImage)
        hbox_buttons.addWidget(self.btn1, alignment=QtCore.Qt.AlignLeft)
        self.btn_search.hide()
        self.btn_search.clicked.connect(self.searchImages)
        
        self.btn_calc = QPushButton("Set Calculation")
        self.btn_calc.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        self.btn_calc.setFixedSize(QtCore.QSize(200, 25))
        self.btn_calc.setStyleSheet("background-color: darkred; color: white; font: bold 14px;")
        self.btn_calc.clicked.connect(calc_set)

        hbox_buttons.addWidget(self.btn_search)
        
        vbox.addLayout(hbox_buttons)
        vbox.addLayout(hbox)
        vbox.addWidget(self.btn_calc)
        self.setLayout(vbox)
        self.show()


        

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Image', './resources/img', "Image files (*.jpg)")
        self.imagePath = fname[0]
        pixmap = QPixmap(self.imagePath)
        #pixmap_resized = pixmap.scaled(400, 400)      
        pixmap_resized = pixmap.scaledToWidth(450)
        self.label.setPixmap(QPixmap(pixmap_resized))
        self.btn_search.show()
        self.btn_calc.hide()
        if self.imagePath=="" :
        	self.btn_search.hide()
        	self.btn_calc.show()  
        self.labelImage1.hide()
        self.labelImage2.hide()
        self.labelImage3.hide()
        self.resize(500,500)
        self.adjustSize()
        self.adjustSize()   #???
        self.move(750,300)
        

        
    def searchImages(self):
        self.searchSimilar()

        pixmap = QPixmap(self.sim_img_1)
        #pixmap_resized = pixmap.scaled(400, 400)
        pixmap_resized = pixmap.scaledToWidth(450)
        self.labelImage1.setPixmap(QPixmap(pixmap_resized))
        self.labelImage1.show()
        #self.labelImage1.setStyleSheet("border: 2px solid black;")
        pixmap2 = QPixmap(self.sim_img_2)
        #pixmap_resized2 = pixmap2.scaled(400, 400)
        pixmap_resized2 = pixmap2.scaledToWidth(450)
        self.labelImage2.setPixmap(QPixmap(pixmap_resized2))
        self.labelImage2.show()
        #self.labelImage2.setStyleSheet("border: 2px solid black;")
        pixmap3 = QPixmap(self.sim_img_3)
        #pixmap_resized3 = pixmap3.scaled(400, 400)
        pixmap_resized3 = pixmap3.scaledToWidth(450)
        self.labelImage3.setPixmap(QPixmap(pixmap_resized3))
        self.labelImage3.show()
        #self.labelImage3.setStyleSheet("border: 2px solid black;")
        self.btn_search.hide()
        self.setGeometry(self.left, self.top, self.width, self.height)
   


    def get_hist(self, img):
    	img = color.rgb2gray(img)
    	img_lbp = local_binary_pattern(img,16,2,'default')
    	h = np.histogram(img_lbp, bins=256, density=True)
    	return h[0]


    def searchSimilar(self):
    	resources = os.path.join(os.getcwd(), 'resources')
    	hists = np.genfromtxt(os.path.join(resources, 'histograms.csv'), delimiter=',')
    	myfiles = np.load(os.path.join(resources, 'myfiles.npy'))
    	#index imagine selectata
    	pImage = self.get_hist(plt.imread(self.imagePath))
    	dists = np.linalg.norm(hists - pImage, axis=1)

    	#cele 3 imagini similare:
    	first_sim_index = np.argsort(dists)[1]
    	first_sim_image = plt.imread(myfiles[first_sim_index])
    	height, width, channel = first_sim_image.shape
    	bytesPerLine = 3 * width
    	self.sim_img_1 = QImage(first_sim_image.data, width, height, bytesPerLine, QImage.Format_RGB888)

    	second_sim_index = np.argsort(dists)[2]
    	second_sim_image = plt.imread(myfiles[second_sim_index])
    	height, width, channel = second_sim_image.shape
    	bytesPerLine = 3 * width
    	self.sim_img_2 = QImage(second_sim_image.data, width, height, bytesPerLine, QImage.Format_RGB888)

    	third_sim_index = np.argsort(dists)[3]
    	third_sim_image = plt.imread(myfiles[third_sim_index])
    	height, width, channel = third_sim_image.shape
    	bytesPerLine = 3 * width
    	self.sim_img_3 = QImage(third_sim_image.data, width, height, bytesPerLine, QImage.Format_RGB888)



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window_program = Window()
    sys.exit(App.exec())