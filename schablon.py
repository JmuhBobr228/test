import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from untitled import Ui_MainWindow
from PyQt5.QtGui import QIcon
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  
from PIL import Image
from PIL.ImageQt import ImageQt  # Для перенесення графіки з Pillow до QT
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
)

workdir = ""

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, ext):
    result = []
    for f in files:
        for e in ext:
            if f.endswith(e):
                result.append(f)
    return result

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Mod/"

    def LoadImage(self, filename):
        self.filename = filename
        fullpath = os.path.join(workdir, filename)
        self.image = Image.open(fullpath)

    def save_image(self):
        full_path = os.path.join(workdir, self.save_dir)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        full_name = os.path.join(full_path, self.filename)
        self.image.save(full_name)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        ex.show_image(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        ex.show_image(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        ex.show_image(image_path)

    def do_rotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        ex.show_image(image_path)

    def do_start(self):
        self.LoadImage(self.filename)
        image_path = os.path.join(workdir, self.filename)
        ex.show_image(image_path)

workimage = ImageProcessor()

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget.currentRowChanged.connect(self.show_choosen_image)
        self.ui.pushButton_3.clicked.connect(workimage.do_bw)
        self.ui.pushButton.clicked.connect(workimage.do_flip)
        self.ui.pushButton_2.clicked.connect(workimage.do_sharp)
        self.ui.pushButton_4.clicked.connect(workimage.do_rotate)
        self.ui.pushButton_5.clicked.connect(workimage.do_start)

    def show_choosen_image(self):
        filename = self.ui.listWidget.currentItem().text()
        workimage.LoadImage(filename)
        self.show_image(os.path.join(workdir, workimage.filename))

    def show_image(self, path):
        self.ui.label.hide()
        pixmap = QPixmap(path)
        width = self.ui.label.width()
        height = self.ui.label.height()
        pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.label.setPixmap(pixmap)
        self.ui.label.show()

app = QApplication(sys.argv)
ex = Widget()
ex.show()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    ex.ui.listWidget.clear()
    for filename in filenames:
        ex.ui.listWidget.addItem(filename)

ex.ui.pushButton_6.clicked.connect(showFilenamesList)

sys.exit(app.exec_())