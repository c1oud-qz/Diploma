import numpy as np
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QBrush, QPen, QPainter, QPolygon, QIcon
from PyQt5.QtCore import QPoint, Qt, QRect

check = True
file_counter = 1
points_arr = []
polygon_points = QPolygon([])
class Window(QMainWindow):
    global file_counter
    path_test = "assets\\test\\"
    path_test_photo = path_test+"RM_gram\\"

    item_number = 0
    imgs = []
    for filename in os.listdir(path_test_photo):
        if os.path.isfile(os.path.join(path_test_photo, filename)):
            imgs.append(filename)
    print(imgs)
    main_file_path = path_test_photo+imgs[item_number]

    def __init__(self):
        super().__init__()
        global check
        global file_counter
        self.setWindowTitle("PyQt5 Drawing Polygon After Pressing")
        window = QWidget(self)
        self.setCentralWidget(window)
        self.checkbox = QCheckBox("Hightlight mode")
        self.checkbox.setChecked(True)
        button = QPushButton("Save object to file")
        layout = QVBoxLayout()

        next_picture_button = QPushButton(">")
        next_picture_button.setFixedSize(60,60)

        window.setLayout(layout)

        self.image_lb = MyLabel(self)
        self.image_photo = QPixmap(self.main_file_path)
        self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
        self.image_lb.setPixmap(self.scaled_pixmap)

        layout.addWidget(next_picture_button)
        layout.addWidget(self.image_lb)
        layout.addWidget(self.checkbox)
        layout.addWidget(button)
        
        next_picture_button.clicked.connect(self.changePicture)
        self.checkbox.stateChanged.connect(self.checkingMode)
        button.clicked.connect(self.saveToFile)
        self.setLayout(layout)
        print(f"file number: {file_counter}")
        self.show()
    def changePicture(self):
        global file_counter
        if self.item_number!=(len(self.imgs)-1):
            self.item_number += 1
        else:
            self.item_number = 0
        file_counter = self.item_number+1
        print(f"file number: {file_counter}")
        self.main_file_path = self.path_test_photo+self.imgs[self.item_number]
        self.image_photo = QPixmap(self.main_file_path)
        self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
        self.image_lb.setPixmap(self.scaled_pixmap)
        self.update()
    def saveToFile(self):
        dialog = Dialog(self)

    def checkingMode(self):
        global check 
        if self.checkbox.isChecked():
            check = True
            print(check)
        else:
            check = False
            print(check)

class Dialog(QDialog):
    name = ""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Object")
        self.setFixedSize(300,150)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.button_clicked)
        self.buttonBox.rejected.connect(self.reject)
        label = QLabel("Введите название выделенного объекта: ")
        self.textEdit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.show()
    def button_clicked(self):
        global file_counter
        global points_arr
        global polygon_points
        print(points_arr)
        self.update()
        if points_arr:
            self.name = self.textEdit.toPlainText()
            obj = ObjectInfo(self.name, points_arr, file_counter)
            obj.printToFile()
        points_arr.clear()
        polygon_points.clear()
        self.update()
        self.close()

    # def coordsToIntArray(self, coord_arr):
    #     arr = []
    #     x, y = 0, 0
    #     for i in coord_arr:
    #         x = coord_arr[i].x()
    #         y = coord_arr[i].y()
    #         arr.append(x, y)
    #     return arr

class ObjectInfo():
    name = ""
    list_coord = []
    filenumber = 0
    def __init__(self, n, lst, filen):
        self.name = n
        self.list_coord = lst
        self.filenumber = filen
    def printToFile(self):
        adres = f"E:\\Diploma\\xray__filters\\objects\\{self.filenumber}.txt"
        with open(adres, "a") as src_f:
            line = f"{self.name}|"
            for item in self.list_coord:
                line += f"{item[0]}|{item[1]}|"
            line += "\n"
            src_f.write(line)
            print(line)
    def deleteFile(self):
        os.remove(f"E:\\Diploma\\xray__filters\\objects\\{self.filenumber}.txt")
    # def clearPolygon(self):


class MyLabel(QLabel):
    def __init__(self, parent=None):
        global polygon_points
        super().__init__(parent)
        self.points_xy = []
        polygon_points = QPolygon([])

    def setPoints(self, points):
        global polygon_points
        self.points = points
        polygon_points = points
        self.update()

    def paintEvent(self, event):
        global check
        global polygon_points
        super().paintEvent(event)
        if check and self.pixmap() is not None:
            painter = QPainter(self)
            pen = QPen(Qt.red, 4, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(Qt.yellow, Qt.VerPattern))
            # for point in self.points_xy:
            #     painter.drawPoint(point)
            painter.drawPolygon(polygon_points)
    def mousePressEvent(self, event):
        global check
        global points_arr
        global polygon_points
        if check and event.button() == Qt.LeftButton and self.pixmap() is not None:
            x = event.x()
            y = event.y()
            points_arr.append((x, y))
            point = QPoint(x, y)
            self.points_xy.append(point)
            polygon_points.append(point)
            self.update()
            print("Coordinates of left mouse button click:", x, y)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())