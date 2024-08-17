from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication, QMessageBox, QFrame,
    QDesktopWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QSize, QRectF, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QTransform, QRegion, QColor, QLinearGradient, QPen
from setools.diff import bounds

from Config import Config


class ApiKeyConfigPage(QWidget):
    # 定义关闭信号
    closed = pyqtSignal()
    def __init__(self, parent=None):
        super(ApiKeyConfigPage, self).__init__(parent)
        layout = QVBoxLayout(self)  # 包含顶栏和主要内容
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint) #Qt.Dialog主要用于在任务栏隐藏图标
        self.resize(450, 350)
        
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # 顶部栏
        top_bar = self.create_top_bar()
        layout.addWidget(top_bar)
        
        #主要内容
        self.setting_main_window =  ApiKeyConfigMainWindow()
        layout.addWidget(self.setting_main_window)

        
        layout.setContentsMargins(0, 0, 0, 0)
        
           
    def create_top_bar(self):
        setting_page_title = BoxTitle(self)

        #创建顶部栏
        top_bar_layout = QHBoxLayout()

        title_label = QLabel("设置")
        title_label.setStyleSheet("font-size: 16px; color: black;")

        close_btn = QPushButton()
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet(
            '''
            QPushButton{background-color:transparent;border:none;color:white;}
            '''
        )

        close_btn.setIcon(QIcon('./data/close.png'))
        close_btn.setIconSize(QSize(24, 24));
        close_btn.clicked.connect(self.close)
        close_btn.setFixedSize(24, 24)

        top_bar_layout.addWidget(title_label)
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(close_btn)

        setting_page_title.setLayout(top_bar_layout) 
        
        return setting_page_title
    
    
    def move_to_center(self):
        #移动到窗口中心位置
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

        # 计算窗口移动位置到屏幕右下角
        right = target_screen_geometry.right()
        bottom = target_screen_geometry.bottom()
        self.move(right/2 - self.width()/2, bottom/2 - self.height()/2)
        
    #鼠标移动，拖拽窗口实现
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if(self.moving):
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if(event.button() == Qt.LeftButton):
            self.moving = False

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
    
    def closeEvent(self, event):
        # 重写关闭事件，以便在关闭时通知父窗口
        self.closed.emit()
        super().closeEvent(event)


class ApiKeyConfigMainWindow(QWidget):
    def __init__(self, parent=None):
        super(ApiKeyConfigMainWindow, self).__init__(parent)
        self.resize(490, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint) #Qt.Dialog主要用于在任务栏隐藏图标

        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 实现圆角
        self.setObjectName('mainwindow')
        self.radius = 15

        # 内容框
        main_layout = QVBoxLayout(self)


        # 创建服务配置项的输入框，并存储它们的引用
        self.bailian_service_box, self.bailian_inputs = self.create_service_box(
            "百炼-问答绘画服务", [("api-key", "API Key")]
        )
        main_layout.addWidget(self.bailian_service_box)

        self.tongyi_service_box, self.tongyi_inputs = self.create_service_box(
            "通义听悟·会议纪要服务",
            [("app-key", "App Key"), ("access key id", "Access Key ID"),
             ("access key secret", "Access Key Secret")])

        #加入主布局中
        main_layout.addWidget(self.tongyi_service_box)

        # 确定和清空框
        button_layout = self.create_buttons()
        main_layout.addLayout(button_layout)

    def create_ai_model_section(self):
        # ai大模型
        ai_model_layout = QVBoxLayout()
        ai_model_layout.setSpacing(15)
        ai_model_layout.setContentsMargins(10, 10, 10, 10)

        ai_model_label = QLabel("AI大模型")
        ai_model_label.setStyleSheet("font-weight: bold;")
        ai_model_layout.addWidget(ai_model_label)


        return ai_model_layout

    def create_service_box(self, service_name, fields):
        # 服务配置项
        service_box = QWidget()
        service_box_layout = QVBoxLayout(service_box)
        service_box_layout.setSpacing(10)

        service_label = QLabel(service_name)
        service_label.setStyleSheet("font-weight: bold; font-size:16px;")
        service_box_layout.addWidget(service_label)


        # 创建一个字典来保存字段名称与对应的 QLineEdit 控件
        field_inputs = {}

        for field_name, placeholder in fields:
            field_label = QLabel(field_name)
            field_input = QLineEdit()

            # 检查配置文件中是否存在该键
            existing_value = None
            if field_name == "api-key":
                existing_value = Config.get_api_key()
            elif field_name == "app-key":
                existing_value = Config.get_app_key()
            elif field_name == "access key id":
                existing_value = Config.get_ALIBABA_CLOUD_ACCESS_KEY_ID()
            elif field_name == "access key secret":
                existing_value = Config.get_ALIBABA_CLOUD_ACCESS_KEY_SECRET()

            # 根据是否存在键来设置 placeholder
            if existing_value:
                field_input.setPlaceholderText(f"已存在{field_name}，输入将会覆盖原有{field_name}")
            else:
                field_input.setPlaceholderText(placeholder)

            # 保存输入框的引用
            field_inputs[field_name] = field_input
            service_box_layout.setContentsMargins(20,0,20,0)

            service_box_layout.addWidget(field_input)

        service_box.setStyleSheet(
            "QWidget { border: none; border-radius: 8px; padding: 10px; }"
        )

        return service_box, field_inputs

    def create_buttons(self):
        # 确定和清空按钮
        button_layout = QHBoxLayout()

        clear_button = QPushButton("清空")
        clear_button.setStyleSheet(
            "background-color: #f0f0f0; color: #4d4f53; font-weight: bold; padding: 10px 20px; border-radius: 5px;border:0.5px solid #7d7d7d"
        )
        clear_button.setFixedWidth(80)
        clear_button.clicked.connect(self.clear_inputs)

        confirm_button = QPushButton("确认")
        confirm_button.setStyleSheet(
            "background-color: #00aaff; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
        )
        confirm_button.setFixedWidth(80)
        confirm_button.clicked.connect(self.confirm)


        button_layout.addStretch(1)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(confirm_button)
        button_layout.setContentsMargins(0, 150, 0, 0)

        return button_layout


    def confirm(self):
        # 从字段字典中获取 QLineEdit 控件的值
        bailian_api_key = self.bailian_inputs['api-key'].text()
        tongyi_app_key = self.tongyi_inputs['app-key'].text()
        tongyi_access_key_id = self.tongyi_inputs['access key id'].text()
        tongyi_access_key_secret = self.tongyi_inputs['access key secret'].text()

        # 输出结果
        # print(f"百炼 API Key: {bailian_api_key}")
        # print(f"通义 App Key: {tongyi_app_key}")
        # print(f"通义 Access Key ID: {tongyi_access_key_id}")
        # print(f"通义 Access Key Secret: {tongyi_access_key_secret}")

        if not bailian_api_key and not tongyi_app_key and not tongyi_access_key_id and not tongyi_access_key_secret:
            QMessageBox.warning(self, "警告", "请输入至少一个API Key或App Key或Access Key ID或Access Key Secret")
            return

        # 检查并设置配置，记录成功或失败的状态
        success = True

        if bailian_api_key:
            if not Config.set_api_key(bailian_api_key):
                success = False

        if tongyi_app_key:
            if not Config.set_app_key(tongyi_app_key):
                success = False

        if tongyi_access_key_id:
            if not Config.set_ALIBABA_CLOUD_ACCESS_KEY_ID(tongyi_access_key_id):
                success = False

        if tongyi_access_key_secret:
            if not Config.set_ALIBABA_CLOUD_ACCESS_KEY_SECRET(tongyi_access_key_secret):
                success = False

        # 弹出结果提示框
        if success:
            QMessageBox.information(self, "配置成功", "所有配置项已成功保存。")
        else:
            QMessageBox.warning(self, "配置失败", "部分配置项保存失败，请重试。")

    def clear_inputs(self):
        # 清空按钮
        for widget in self.findChildren(QLineEdit):
            widget.clear()
        
        
class BoxTitle(QWidget):
    def __init__(self, *args, **kwargs):
        super(BoxTitle, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('box_title')
        self.setStyleSheet(
                '''
                #box_title{
                    border-left: 2px solid transparent;
                    border-top-left-radius: 15px;
                    border-top-right-radius: 15px;
                    background-color: white;
                    background-clip: padding-box; 
                }
                '''
            )
        self.installEventFilter(self)
        self.setFixedHeight(36)


# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     api_key_config_page = ApiKeyConfigPage()
#     api_key_config_page.show()
#     sys.exit(app.exec_())
