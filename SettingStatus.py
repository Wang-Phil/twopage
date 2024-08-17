from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QColor, QLinearGradient, QPen


class StatusDialog(QWidget):
    def __init__(self, success=True):
        super().__init__()

        self.setFixedSize(400, 200)
        self.move_to_center()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 主布局
        main_layout = QVBoxLayout()

        # 添加各个部分到主布局
        main_layout.addLayout(self.create_close_button())
        main_layout.addLayout(self.create_icon_and_title(success))
        main_layout.addLayout(self.create_detail_info(success))
        main_layout.addLayout(self.create_confirm_button())


        # 设置窗口样式
        self.setStyleSheet("background-color: white; border-radius: 10px;")
        self.setLayout(main_layout)


    def create_close_button(self):
        # 关闭按钮
        close_button = QPushButton("×")
        close_button.setFont(QFont('Arial', 12))
        close_button.setStyleSheet("border: none; color: gray;")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close)

        # 关闭按钮的布局
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch(1)
        close_button_layout.addWidget(close_button)
        return close_button_layout
    def create_icon_and_title(self, success):
        # 水平布局：图标 + 状态消息
        status_layout = QHBoxLayout()

        # 图标
        icon_label = QLabel()
        icon_pixmap = QPixmap('success_icon.png').scaled(30, 30, Qt.KeepAspectRatio) if success else QPixmap(
            'error_icon.png').scaled(30, 30, Qt.KeepAspectRatio)
        icon_label.setPixmap(icon_pixmap)

        # 状态标题
        status_label = QLabel("配置成功" if success else "配置失败")
        status_label.setFont(QFont('Arial', 14, QFont.Bold))
        status_label.setStyleSheet("color: black;")

        # 添加图标和状态消息到布局中
        status_layout.addWidget(icon_label)
        status_layout.addWidget(status_label)
        status_layout.addStretch(1)
        status_layout.setContentsMargins(30, 0, 10, 0)
        return status_layout

    def create_detail_info(self, success):
        # 水平布局：详细信息
        detail_layout = QHBoxLayout()

        # 状态详细信息
        detail_label = QLabel("所有配置项已成功保存" if success else "所有配置项保存失败")
        detail_label.setFont(QFont('Arial', 11))
        detail_label.setStyleSheet("color: gray;")

        # 将详细信息添加到布局中
        detail_layout.addWidget(detail_label)
        detail_layout.addStretch(1)
        detail_layout.setContentsMargins(45, 0, 10, 45)
        return detail_layout

    def create_confirm_button(self):
        # 确定按钮
        confirm_button = QPushButton("确定")
        confirm_button.setFont(QFont('Arial', 12))
        confirm_button.setFixedSize(130, 40)  # 宽度为100像素，高度为40像素
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 5px 20px;
            }
            }
        """)
        confirm_button.clicked.connect(self.close)

        # 确定按钮的布局
        confirm_button_layout = QHBoxLayout()
        confirm_button_layout.addStretch(1)
        confirm_button_layout.addWidget(confirm_button)
        confirm_button_layout.setContentsMargins(0, 0, 20, 10)
        return confirm_button_layout

    def paintEvent(self, event):
        #画圆角
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 设置抗锯齿，让圆角更加平滑
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        painter.setPen(QColor(0, 0, 0, 10))  # 黑色，透明度设置为10
        painter.setBrush(self.palette().window().color())#设置画刷为窗口背景颜色
        radius = 15 #设置圆角半径

        bounds = self.rect()  # 获取窗口的边界
        # 绘制阴影
        shadow = QLinearGradient(bounds.topLeft(), bounds.bottomLeft())
        shadow.setColorAt(0, QColor(100, 100, 100, 50))

        # 设置阴影的模糊半径
        painter.setPen(QPen(shadow, 1))
        painter.drawRoundedRect(self.rect(), radius, radius)

    def move_to_center(self):
        # 获取屏幕总数和屏幕几何数据
        desktop = QDesktopWidget()
        screen_count = desktop.screenCount()
        if screen_count > 1:
            # 多屏情况下，用第一个屏幕
            target_screen_index = 0
            # 获取目标屏幕的几何信息
            target_screen_geometry = desktop.screenGeometry(target_screen_index)
        else:
            # 单屏情况下使用默认屏幕
            target_screen_geometry = desktop.screenGeometry()

        # 计算窗口移动位置到屏幕中心
        right = target_screen_geometry.width()
        bottom = target_screen_geometry.height()
        self.move(int(right / 2 - self.width() / 2), int(bottom / 2 - self.height() / 2))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # 创建对话框实例，传入 True 显示成功信息，传入 False 显示失败信息
    success_dialog = StatusDialog(success=True)
    success_dialog.show()

    sys.exit(app.exec_())
