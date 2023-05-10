import sys
import random
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PaintBoard import PaintBoard
class RandomNamePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Random Name Picker')
        self.setGeometry(100, 100, 400, 300)
        self.names = []  # 姓名列表
        # 随机点名按钮
        self.random_name_btn = QPushButton('点名', self)
        self.random_name_btn.clicked.connect(self.pick_random_name)

        # 读取Excel文件按钮
        self.import_names_btn = QPushButton('导入名单', self)
        self.import_names_btn.clicked.connect(self.import_names_from_excel)

        # 画板
        self.btn = QPushButton('画板', self)
        self.btn.clicked.connect(self.slot_btn_function)

        # 显示结果的标签
        self.result_label = QLabel(self)

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.import_names_btn)
        vbox.addWidget(self.random_name_btn)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.result_label)
        self.setLayout(vbox)
    def slot_btn_function(self):

        self.s = PaintBoard()  # 将第二个窗口换个名字
        self.s.setWindowTitle('Mouse Paint')
        self.s.setGeometry(100, 100, 800, 600)
        self.s.show()  # 经第二个窗口显示出来



    def pick_random_name(self):

        random_name = random.choice(self.names)
        self.names.remove(random_name)
        self.result_label.setText(f'被选中的姓名是：{random_name}')
        if not self.names:
            self.result_label.setText(f"点完名了！")

    def import_names_from_excel(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, '选择Excel文件', '',
                                                   'Excel Files (*.xlsx *.xls)', options=options)
        if file_name:
            try:
                df = pd.read_excel(file_name)
                self.names = df['姓名'].tolist()
                self.result_label.setText(f'已导入名单，共{len(self.names)}人')
            except Exception as e:
                self.result_label.setText(f'导入失败，错误信息：{e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    picker = RandomNamePicker()
    picker.show()
    sys.exit(app.exec_())

