import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel
import torch
import torchvision
from PIL import Image, ImageOps

#分类识别网络
MODEL_PATH = './weight/MyCNN_MNIST.pkl'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(MODEL_PATH).to(DEVICE)

class PaintBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个文字栏
        self.label = QLabel(self)
        self.label.setFont(QFont("Arial", 20))  # 设置字体为Arial，大小为20
        self.label.setGeometry(50,50,200,50)
        self.setCentralWidget(self.label)

        # 创建一个画板
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # 初始化画笔
        self.pen = QPen(Qt.black, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        # 创建一个菜单栏
        menu_bar = self.menuBar()

        # 添加文件菜单
        file_menu = menu_bar.addMenu('File')

        # 添加保存图片的动作
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)

        # 添加清空画板的动作
        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)
        file_menu.addAction(clear_action)

        # 添加输出图片动作
        recognize_action = QAction('Recognize', self)
        recognize_action.triggered.connect(self.on_btn_Recognize_Clicked)
        menu_bar.addAction(recognize_action)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False

    def on_btn_Recognize_Clicked(self):
        savePath = "./text.png"
        self.image.save(savePath)
        image = Image.open(savePath).convert("1")
        image = ImageOps.invert(image)
        image = image.resize((28, 28), Image.Resampling.LANCZOS)
        image = torchvision.transforms.ToTensor()(image).unsqueeze(0)
        image = image.to(DEVICE)
        outputs = model(image)
        pred = torch.max(outputs, 1)[1]
        self.label.setText(f'识别数字为：{pred[0].item()}')

    def clear(self):
        self.image.fill(Qt.white)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaintBoard()
    window.setWindowTitle('Mouse Paint')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
