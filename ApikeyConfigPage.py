from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ApiKeyConfigPage(QWidget):
    def __init__(self, parent=None):
        super(ApiKeyConfigPage, self).__init__(parent)

        self.setWindowTitle("配置")
        self.resize(500, 450)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top bar with title and close button
        top_bar = self.create_top_bar()
        main_layout.addLayout(top_bar)

        # AI model configuration section
        ai_model_section = self.create_ai_model_section()
        main_layout.addLayout(ai_model_section)

        # Confirm and Clear buttons
        button_layout = self.create_buttons()
        main_layout.addLayout(button_layout)

    def create_top_bar(self):
        # Top bar layout
        top_bar_layout = QHBoxLayout()

        # Title label
        title_label = QLabel("配置")
        title_label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")

        # Close button
        close_button = QPushButton("关闭")
        close_button.setStyleSheet(
            "QPushButton { border: none; background-color: transparent; color: gray; }"
        )
        close_button.clicked.connect(self.close)

        # Add widgets to the layout
        top_bar_layout.addWidget(title_label)
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(close_button)

        return top_bar_layout

    def create_ai_model_section(self):
        # AI model section layout
        ai_model_layout = QVBoxLayout()
        ai_model_layout.setSpacing(15)
        ai_model_layout.setContentsMargins(10, 10, 10, 10)

        # AI model header
        ai_model_label = QLabel("AI大模型")
        ai_model_label.setStyleSheet("font-weight: bold;")
        ai_model_layout.addWidget(ai_model_label)

        # BaiLian Service configuration
        bailian_service_box = self.create_service_box(
            "百炼-问答绘图服务", [("api-key", "输入API Key")]
        )
        ai_model_layout.addWidget(bailian_service_box)

        # TongYi Service configuration
        tongyi_service_box = self.create_service_box(
            "通义听悟·会议纪要服务",
            [("app-key", "输入App Key"), ("access key id", "输入Access Key ID"), ("access key secret", "输入Access Key Secret")]
        )
        ai_model_layout.addWidget(tongyi_service_box)

        return ai_model_layout

    def create_service_box(self, service_name, fields):
        # Service box widget
        service_box = QWidget()
        service_box_layout = QVBoxLayout(service_box)
        service_box_layout.setSpacing(10)

        # Service name label
        service_label = QLabel(service_name)
        service_label.setStyleSheet("font-weight: bold;")
        service_box_layout.addWidget(service_label)

        # Field inputs
        for field_name, placeholder in fields:
            field_label = QLabel(field_name)
            field_input = QLineEdit()
            field_input.setPlaceholderText(placeholder)

            service_box_layout.addWidget(field_label)
            service_box_layout.addWidget(field_input)

        # Style for service box
        service_box.setStyleSheet(
            "QWidget { border: 1px solid lightgray; border-radius: 8px; padding: 10px; }"
        )

        return service_box

    def create_buttons(self):
        # Button layout
        button_layout = QHBoxLayout()

        # Confirm button
        confirm_button = QPushButton("确认")
        confirm_button.setStyleSheet(
            "background-color: #00aaff; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
        )
        confirm_button.setFixedWidth(80)
        confirm_button.clicked.connect(self.confirm)

        # Clear button
        clear_button = QPushButton("清空")
        clear_button.setStyleSheet(
            "background-color: #f0f0f0; color: black; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
        )
        clear_button.setFixedWidth(80)
        clear_button.clicked.connect(self.clear_inputs)

        # Add buttons to layout
        button_layout.addStretch(1)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(clear_button)

        return button_layout


    def confirm(self):
        # Placeholder for confirm logic
        print("确认按钮点击")

    def clear_inputs(self):
        # Logic to clear all inputs
        for widget in self.findChildren(QLineEdit):
            widget.clear()

# Run the application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    api_key_config_page = ApiKeyConfigPage()
    api_key_config_page.show()
    sys.exit(app.exec_())
