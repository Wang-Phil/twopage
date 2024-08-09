from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from Config import Config


class ApiKeyConfigPage(QWidget):
    def __init__(self, parent=None):
        super(ApiKeyConfigPage, self).__init__(parent)
        self.resize(500, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top bar with title and close button
        top_bar = self.create_top_bar()
        main_layout.addLayout(top_bar)

        # 创建服务配置项的输入框，并存储它们的引用
        # 创建服务配置项的输入框，并存储它们的引用
        self.bailian_service_box, self.bailian_inputs = self.create_service_box(
            "百炼-问答绘图服务", [("api-key", "输入API Key")]
        )
        main_layout.addWidget(self.bailian_service_box)

        self.tongyi_service_box, self.tongyi_inputs = self.create_service_box(
            "通义听悟·会议纪要服务",
            [("app-key", "输入App Key"), ("access key id", "输入Access Key ID"),
             ("access key secret", "输入Access Key Secret")])
        main_layout.addWidget(self.tongyi_service_box)

        # Confirm and Clear buttons
        button_layout = self.create_buttons()
        main_layout.addLayout(button_layout)

    def create_top_bar(self):
        # Top bar layout
        top_bar_layout = QHBoxLayout()

        # 提示
        title_label = QLabel("配置")
        title_label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")

        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.setStyleSheet(
            "QPushButton { border: none; background-color: transparent; color: gray; }"
        )
        close_button.clicked.connect(self.close)


        top_bar_layout.addWidget(title_label)
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(close_button)

        return top_bar_layout

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
        service_box = QWidget()
        service_box_layout = QVBoxLayout(service_box)
        service_box_layout.setSpacing(10)

        service_label = QLabel(service_name)
        service_label.setStyleSheet("font-weight: bold;")
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

            service_box_layout.addWidget(field_label)
            service_box_layout.addWidget(field_input)

        service_box.setStyleSheet(
            "QWidget { border: 1px solid lightgray; border-radius: 8px; padding: 10px; }"
        )

        return service_box, field_inputs

    def create_buttons(self):

        button_layout = QHBoxLayout()


        confirm_button = QPushButton("确认")
        confirm_button.setStyleSheet(
            "background-color: #00aaff; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
        )
        confirm_button.setFixedWidth(80)
        confirm_button.clicked.connect(self.confirm)


        clear_button = QPushButton("清空")
        clear_button.setStyleSheet(
            "background-color: #f0f0f0; color: black; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
        )
        clear_button.setFixedWidth(80)
        clear_button.clicked.connect(self.clear_inputs)


        button_layout.addStretch(1)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(clear_button)

        return button_layout


    def confirm(self):
        # 从字段字典中获取 QLineEdit 控件的值
        bailian_api_key = self.bailian_inputs['api-key'].text()
        tongyi_app_key = self.tongyi_inputs['app-key'].text()
        tongyi_access_key_id = self.tongyi_inputs['access key id'].text()
        tongyi_access_key_secret = self.tongyi_inputs['access key secret'].text()\

        # 输出结果
        print(f"百炼 API Key: {bailian_api_key}")
        print(f"通义 App Key: {tongyi_app_key}")
        print(f"通义 Access Key ID: {tongyi_access_key_id}")
        print(f"通义 Access Key Secret: {tongyi_access_key_secret}")

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

        # 可以添加一些逻辑来通知用户保存成功，或者更新UI等
        print("配置已保存")

    def clear_inputs(self):
        # 清空按钮
        for widget in self.findChildren(QLineEdit):
            widget.clear()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    api_key_config_page = ApiKeyConfigPage()
    api_key_config_page.show()
    sys.exit(app.exec_())
