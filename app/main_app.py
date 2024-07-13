import numpy as np
import os
import cv2
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPolygon, QImage
from PyQt5.QtCore import QPoint, Qt, QRect
import sys

isPhotoMode = True
file_counter = 1
object_number = 0
obj_list = []
crd_list = []
poly_list = QPolygon([])
count_results = 0
class test_main_app(QMainWindow):
    global file_counter
    path_icons = "assets\\icons\\"
    path_test = "assets\\test\\"
    path_test_RMG = path_test+"RM_gram\\"
    path_test_photo = path_test+"Photo\\"
    imgs = []
    for filename in os.listdir(path_test_photo):
        if os.path.isfile(os.path.join(path_test_photo, filename)):
            imgs.append(filename)
    print(imgs)
    
    main_file_path = path_test_photo+imgs[file_counter-1]
    
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets\\window.png"))
        self.initializeUI()
        self.introMsg()
    def introMsg(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Описание")
        explanation = "Внимательно изучите представленные на фотографиях предметы и их свойства. Для начала теста нажмите кнопку 'Рентген', чтобы переключиться на рентгеновский слой. На этом шаге Вам будет представлено рентгенографическое изображение и список предметов, расположение которых необходимо правильно определить. Для этого выберите «Найти объекты», после чего найдите предложенный предмет на изображении и щелкните по нему с помощью ЛКМ. С правой стороны имеется группа кнопок, предоставляющая различные фильтры. Определив все предметы, нажмите кнопку '>' для перехода к следующему изображению."
        dlg.setText(explanation)
        dlg.exec()
    def initializeUI(self):
        desktop = QApplication.desktop()
        screen = desktop.availableGeometry()
        width = screen.width()
        height = screen.height()
        self.setGeometry(QRect(0, 0, width, height))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Filter Tests")
        self.addLayouts()
        self.showMaximized()
        self.filter = Filters()
    def addLayouts(self):
        layout = QHBoxLayout()
        self.central_widget.setLayout(layout)
        # Left Layout (Menu Bar)
        left_widget = QWidget() 
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(200)
        # left_widget.setStyleSheet("background-color: blue")
        left_layout.setContentsMargins(10, 10, 10, 10)
        icons = []
        for i in range(5):
            icons.append(f"{self.path_icons}icon{i+1}.png")
        # icons = [path_icons+"icon1.png", path_icons+"icon2.png", path_icons+"icon3.png", path_icons+"icon4.png"]
        
        # for icon in icons:
        #     action = QAction(QIcon(f"assets/{icon}"), icon, self)
        #     self.left_layout.addAction(action)
        for icon in icons:
            icon_label = QLabel()
            pixmap = QPixmap(icon)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(icon_label)

        # Right widget (Image)
        right_widget = QWidget() 
        top_layout = QVBoxLayout()
        # top_layout.addStretch()

        self.center_layout = QVBoxLayout()

        top_label = QLabel("ТЕСТИРОВАНИЕ")
        top_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(top_label)

        # Add widgets to top layout
        central_widget = QWidget()
        self.center_label = MyLabel(self)
        # self.center_label.setAlignment(Qt.AlignCenter)
        # self.center_label.setStyleSheet("background-color: red")
        self.center_layout.addWidget(self.center_label)
        self.image_photo = QPixmap(self.main_file_path)
        self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
        self.center_label.setPixmap(self.scaled_pixmap)
        central_widget.setLayout(self.center_layout)
        central_widget.setMaximumWidth(1200)
        top_layout.addWidget(central_widget, alignment=Qt.AlignCenter)

        # Add widgets to bottom layout
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        open_RM_button = QPushButton("Рентген")
        open_RM_button.setFixedSize(150,60)
        
        find_objs_button = QPushButton("Найти объекты")
        find_objs_button.setFixedSize(150,60)
        
        next_picture_button = QPushButton(">")
        next_picture_button.setFixedSize(60,60)

        grid_btm_layout_left = QHBoxLayout()
        grid_btm_layout_left.addWidget(open_RM_button)
        grid_btm_layout_left.addWidget(find_objs_button)
        grid_btm_layout_left.addWidget(next_picture_button)
        grid_btm_layout_left.setAlignment(Qt.AlignRight)

        find_objs_button.clicked.connect(self.find_objs_button_clicked)
        open_RM_button.clicked.connect(self.setRMgram)
        next_picture_button.clicked.connect(self.changePicture)

        bottom_layout.addLayout(grid_btm_layout_left)

        # Кнопки фильтров
        metallic_button = QPushButton("Металл")
        metallic_button.setFixedSize(150,60)
        metallic_button.clicked.connect(self.metallic_button_clicked)
        # bottom_layout.addWidget(metallic_button)

        organic_button = QPushButton("Органика")
        organic_button.setFixedSize(150,60)
        organic_button.clicked.connect(self.organic_button_clicked)
        # bottom_layout.addWidget(organic_button)

        BW_button = QPushButton("Черно-белое")
        BW_button.setFixedSize(150,60)
        BW_button.clicked.connect(self.BW_button_clicked)
        # bottom_layout.addWidget(BW_button)

        negative_button = QPushButton("Негатив")
        negative_button.setFixedSize(150,60)
        negative_button.clicked.connect(self.negative_button_clicked)
        # bottom_layout.addWidget(negative_button)

        contrast_button = QPushButton("Контраст")
        contrast_button.setFixedSize(150,60)
        contrast_button.clicked.connect(self.contrast_button_clicked)
        # bottom_layout.addWidget(contrast_button)

        
        grid_btm_layout_right = QHBoxLayout()
        grid_btm_layout_right.addWidget(metallic_button)
        grid_btm_layout_right.addWidget(organic_button)
        grid_btm_layout_right.addWidget(BW_button)
        grid_btm_layout_right.addWidget(negative_button)
        grid_btm_layout_right.addWidget(contrast_button)
        grid_btm_layout_right.setAlignment(Qt.AlignCenter)
        space = "   "
        space_lb = QLabel(space)
        # space.setStyleSheet("background-color: red")
        bottom_layout.addWidget(space_lb, alignment=Qt.AlignCenter)

        bottom_layout.addLayout(grid_btm_layout_right)
        
        bottom_layout.addStretch(1)
        bottom_layout.setAlignment(Qt.AlignCenter)
        bottom_widget.setLayout(bottom_layout)
        top_layout.addWidget(bottom_widget)

        right_widget.setLayout(top_layout)

        layout.addWidget(left_widget)
        layout.addWidget(right_widget, alignment=Qt.AlignCenter)

    def metallic_button_clicked(self):
        if (not isPhotoMode):
            qimg = self.filter.apply_metallic_filter(self.main_file_path)
            self.image_photo = QPixmap(qimg)
            self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
            self.center_label.setPixmap(self.scaled_pixmap)
        else:
            self.openRM()
    def organic_button_clicked(self):
        if (not isPhotoMode):
            qimg = self.filter.apply_organic_filter(self.main_file_path)
            self.image_photo = QPixmap(qimg)
            self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
            self.center_label.setPixmap(self.scaled_pixmap)
        else:
            self.openRM()
    def BW_button_clicked(self):
        if (not isPhotoMode):
            qimg = self.filter.apply_grayscale_filter(self.main_file_path)
            self.image_photo = QPixmap(qimg)
            self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
            self.center_label.setPixmap(self.scaled_pixmap)
        else:
            self.openRM()
    def negative_button_clicked(self):
        if (not isPhotoMode):
            qimg = self.filter.apply_negative_filter(self.main_file_path)
            self.image_photo = QPixmap(qimg)
            self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
            self.center_label.setPixmap(self.scaled_pixmap)
        else:
            self.openRM()
    def contrast_button_clicked(self):
        if (not isPhotoMode):
            qimg = self.filter.apply_contrast_filter(self.main_file_path)
            self.image_photo = QPixmap(qimg)
            self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
            self.center_label.setPixmap(self.scaled_pixmap)
        else:
            self.openRM()
    def find_objs_button_clicked(self):
        if (not isPhotoMode):
            self.showMessage()
        else:
            self.openRM()
    def setRMgram(self):
        global file_counter, object_number, isPhotoMode, obj_list
        isPhotoMode = False
        # print(isPhotoMode)
        # if (self.main_file_path == self.path_test_photo+self.imgs[self.item_number]):
        self.main_file_path = self.path_test_RMG+self.imgs[file_counter-1]
        self.image_photo = QPixmap(self.main_file_path)
        self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
        self.center_label.setPixmap(self.scaled_pixmap)
        
        this_parse = ParseFile(file_counter)
        obj_list = this_parse.getObjects()

    def showMessage(self):
        global object_number, obj_list
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Задание")
        explanation = f"Отметьте предмет: {obj_list[object_number]}"
        dlg.setText(explanation)
        # dlg.setWordWrap(True)
        dlg.exec()
    def openRM(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Следующий шаг")
        explanation = "Сначала необходимо выбрать рентгеновский слой, нажав на 'Рентген'!"
        dlg.setText(explanation)
        dlg.setIcon(QMessageBox.Critical)
        dlg.exec()

    def changePicture(self):
        global file_counter,isPhotoMode, obj_list, object_number, crd_list, poly_list
        isPhotoMode = True
        
        # print(isPhotoMode)
        if file_counter<(len(self.imgs)-1):
            file_counter += 1
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Результат")
            explanation = f"Правильных ответов: {count_results} из 28"
            dlg.setText(explanation)
            # dlg.setWordWrap(True)
            dlg.exec()
            print("Конец теста!")
        self.main_file_path = self.path_test_photo+self.imgs[file_counter-1]
        self.image_photo = QPixmap(self.main_file_path)
        self.scaled_pixmap = self.image_photo.scaledToWidth(1200)
        self.center_label.setPixmap(self.scaled_pixmap)
        obj_list.clear()
        object_number = 0
        crd_list.clear()
        poly_list.clear()
        self.filter.reset_filters()
        self.update()

class ParseFile():
    file_num = 0
    def __init__(self, flc):
        self.file_num = flc
    def readFile(self):
        data = []
        adres = f"E:\\Diploma\\xray__filters\\objects\\{self.file_num}.txt"
        with open(adres, "r") as src_f:
            lines = src_f.readlines()
            # print(lines)
            for i in lines:
                array = i.split("|")
                data.append(array)
                # print(array)
        return data
    def getObjects(self):
        double_arr = self.readFile()
        objects_arr = []
        for arr in double_arr:
            objects_arr.append(arr[0])
        return objects_arr
    def getCoords(self):
        double_arr = self.readFile()
        coords_arr = []
        for arr in double_arr:
            temp_arr = []
            for i in range(1, len(arr)-1, 2):
                temp_arr.append((int(arr[i]), int(arr[i+1])))
            coords_arr.append(temp_arr)
        return coords_arr
    def getPoly(self, num_obj):
        poly_arr = []
        all_arr = self.getCoords()
        for i in all_arr[num_obj]:
            point = QPoint()
            point.setX(i[0])
            point.setY(i[1])
            # print(point)
            poly_arr.append(point)
        # print(all_arr[file_counter-1])
        return poly_arr
    

class MyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def showDialog(self, txt):
        dlg = QMessageBox(window)
        dlg.setWindowTitle("Задание")
        if (txt == "yes"):
            dlg.setText("Правильно!")
            dlg.setIcon(QMessageBox.Information)
        else:
            dlg.setText("Неправильно!")
            dlg.setIcon(QMessageBox.Critical)
        dlg.exec()
    
    def showMessage(self):
        global object_number, obj_list
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Задание")
        explanation = f"Отметьте предмет: {obj_list[object_number]}"
        dlg.setText(explanation)
        # dlg.setWordWrap(True)
        dlg.exec()

    def mousePressEvent(self, event):
        global file_counter, isPhotoMode, obj_list, crd_list, poly_list, object_number, count_results
        print(object_number)
        this_parse = ParseFile(file_counter)
        obj_list = this_parse.getObjects()
        crd_list = this_parse.getCoords()
        if (not isPhotoMode) and (event.button() == Qt.LeftButton) and (self.pixmap() is not None):
            x = event.x()
            y = event.y()
            mouse_point = QPoint(x, y)
            print("Coordinates of left mouse button click:", mouse_point)
            print(obj_list[object_number])
            for i in crd_list[object_number]:
                point = QPoint()
                point.setX(i[0])
                point.setY(i[1])
                print(point)
                poly_list.append(point)
                print(poly_list)
            # Здесь нужно чекать если попадает внутрь фигуры точка
            if (poly_list.containsPoint(mouse_point, Qt.OddEvenFill)):
                self.showDialog("yes")
                count_results += 1
                print("Точка находится в пределах полигона")
            else:
                self.showDialog("no")
                print("Точка не находится в пределах полигона")
            if object_number<(len(obj_list)-1):
                object_number+=1
                self.showMessage()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle(f"Этап №{file_counter} завершен")
                explanation = f"Переходите к следующей фотографии, нажав кнопку '>'"
                dlg.setText(explanation)
                dlg.exec()
            self.update()

class Filters:

    metallic_filter_applied = False
    organic_filter_applied = False
    grayscale_filter_applied = False
    negative_filter_applied = False
    contrast_filter_applied = False

    # Initialize the lower and upper bounds for the metallic filter
    lower_blue = [0, 0, 0]
    upper_blue = [116, 255, 255]
    lower_black = [0, 0, 0]
    upper_black = [180, 50, 50]

    # Initialize the lower and upper bounds for orange filter
    lower_orange = [0, 50, 30]
    upper_orange = [34, 255, 255]  # Обновленные значения

    # Initialize the lower and upper bounds for green filter
    lower_green = [0, 50, 30]
    upper_green = [0, 0, 0]  # Обновленные значения

    # Initialize contrast factor
    contrast_factor = 1.5

    def reset_filters(self):
        Filters.metallic_filter_applied = False
        Filters.organic_filter_applied = False
        Filters.grayscale_filter_applied = False
        Filters.negative_filter_applied = False
        Filters.contrast_filter_applied = False

    def apply_metallic_filter(self, img_path):
        image = cv2.imread(img_path)
        filtered_image = image.copy()
        hsv_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)

        lower_blue_bound = np.array(Filters.lower_blue)
        upper_blue_bound = np.array(Filters.upper_blue)
        lower_black_bound = np.array(Filters.lower_black)
        upper_black_bound = np.array(Filters.upper_black)

        blue_mask = cv2.inRange(hsv_image, lower_blue_bound, upper_blue_bound)
        black_mask = cv2.inRange(hsv_image, lower_black_bound, upper_black_bound)

        metallic_mask = cv2.bitwise_or(blue_mask, black_mask)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grayscale_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

        canvas = filtered_image.copy()
        canvas[metallic_mask == 255] = grayscale_image[metallic_mask == 255]

        
        Filters.metallic_filter_applied = True
        ret_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        return QImage(ret_canvas, ret_canvas.shape[1], ret_canvas.shape[0], ret_canvas.shape[1] * 3, QImage.Format_RGB888)
    def apply_organic_filter(self, img_path):
        image = cv2.imread(img_path)
        filtered_image = image.copy()
        hsv_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)

        # Определяем диапазоны для оранжевых и остальных цветов на основе указанных значений
        orange_low = np.array(Filters.lower_orange)
        orange_high = np.array(Filters.upper_orange)

        # Создаем маску для оранжевых цветов
        orange_mask = cv2.inRange(hsv_image, orange_low, orange_high)

        # Конвертируем изображение в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Конвертируем изображение в формат с тремя каналами
        grayscale_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

        canvas = filtered_image.copy()
        canvas[orange_mask == 0] = grayscale_image[orange_mask == 0]
        ret_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        Filters.organic_filter_applied = True
        return QImage(ret_canvas, ret_canvas.shape[1], ret_canvas.shape[0], ret_canvas.shape[1] * 3, QImage.Format_RGB888)

    def apply_grayscale_filter(self, img_path):
        image = cv2.imread(img_path)
        filtered_image = image.copy()
        gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        grayscale_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        Filters.grayscale_filter_applied = True
        return QImage(grayscale_image, grayscale_image.shape[1], grayscale_image.shape[0], grayscale_image.shape[1] * 3, QImage.Format_RGB888)
    def apply_negative_filter(self, img_path):
        image = cv2.imread(img_path)
        filtered_image = image.copy()
        gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)
        inverted_image = cv2.bitwise_not(gray_image)
        inverted_image = cv2.cvtColor(inverted_image, cv2.COLOR_GRAY2BGR)
        Filters.negative_filter_applied = True
        return QImage(inverted_image, inverted_image.shape[1], inverted_image.shape[0], inverted_image.shape[1] * 3, QImage.Format_RGB888)
    def apply_contrast_filter(self, img_path):
        image = cv2.imread(img_path)
        filtered_image = image.copy()
        contrasted_image = cv2.convertScaleAbs(filtered_image, alpha=Filters.contrast_factor, beta=0)
        ret_canvas = cv2.cvtColor(contrasted_image, cv2.COLOR_BGR2RGB)
        Filters.contrast_filter_applied = True
        return QImage(ret_canvas, ret_canvas.shape[1], ret_canvas.shape[0], ret_canvas.shape[1] * 3, QImage.Format_RGB888)

        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    style = """
        QLabel{
            font-family: "Verdana";
            font-size: 18px;
            font-weight: 700;
            font-style: italic;
        }
        QPushButton{
            font-family: "Verdana";
            font-size: 15px;
            font-weight: 500;
            font-style: normal;
        }
    """
    app.setStyleSheet(style)
    window = test_main_app()
    sys.exit(app.exec_())        
