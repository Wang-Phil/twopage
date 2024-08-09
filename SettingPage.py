from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ApiKeyConfigPage import ApiKeyConfigPage
from Config import Config


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super(SettingsPage, self).__init__(parent)
        self.resize(500, 350)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Top bar with title and close button
        top_bar = self.create_top_bar()
        main_layout.addLayout(top_bar)

        # 初始化服务状态字典
        self.services_status = {
            "百炼-问答绘图服务": "待添加",
            "通义听悟·会议纪要服务": "待添加"
        }

        # 检查并更新服务状态
        self.check_and_update_services_status()

        # AI model configuration section
        ai_model_section = self.create_ai_model_section()
        main_layout.addLayout(ai_model_section)

        # Model Strategy Button
        model_strategy_button = self.create_model_strategy_button()
        main_layout.addWidget(model_strategy_button)

    def create_top_bar(self):
        # Top bar layout
        top_bar_layout = QHBoxLayout()

        # Title label
        title_label = QLabel("设置")
        title_label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")

        # Close button
        close_button = QPushButton("关闭")
        close_button.setStyleSheet(
            "QPushButton { border: none; background-color: transparent; color: red; }"
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
        ai_model_layout.setSpacing(10)
        ai_model_layout.setContentsMargins(10, 10, 10, 10)

        # AI model header
        header_layout = QHBoxLayout()
        ai_model_label = QLabel("AI大模型")
        configure_button = QPushButton("配置")
        # 添加按钮的点击事件
        configure_button.clicked.connect(self.openApiKeyConfigPage)
        configure_button.setStyleSheet("background-color: lightgray; font-weight: bold;")
        configure_button.setFixedWidth(60)

        header_layout.addWidget(ai_model_label)
        header_layout.addStretch(1)
        header_layout.addWidget(configure_button)

        # Add header layout to AI model layout
        ai_model_layout.addLayout(header_layout)

        # Service statuses
        services_box = self.create_services_box()
        ai_model_layout.addWidget(services_box)

        return ai_model_layout

    def create_services_box(self):
        # Services box layout
        services_box = QWidget()
        services_layout = QVBoxLayout(services_box)
        services_layout.setSpacing(10)


        for service, status in self.services_status.items():
            color = "green" if status == "已添加" else "red"
            service_item_layout = QHBoxLayout()
            service_label = QLabel(service)
            status_label = QLabel(status)
            status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            service_item_layout.addWidget(service_label)
            service_item_layout.addStretch(1)
            service_item_layout.addWidget(status_label)

            # Add service item layout to services layout
            services_layout.addLayout(service_item_layout)

        # Style for services box
        services_box.setStyleSheet(
            "QWidget { border: 1px solid lightgray; border-radius: 8px; padding: 10px; }"
        )

        return services_box

    def create_model_strategy_button(self):
        # Model strategy button
        strategy_button = QPushButton("获取模型攻略")
        strategy_button.setStyleSheet(
            "background-color: #FFCC33; font-weight: bold; padding: 8px; margin-top: 10px;"
        )
        return strategy_button

    def openApiKeyConfigPage(self):
        # 创建并显示 APIKeyConfigPage 窗口
        self.apiKeyConfigPage = ApiKeyConfigPage()
        self.apiKeyConfigPage.show()
        self.hide()

    def check_and_update_services_status(self):
        # 检查百炼-问答绘图服务的API Key是否已配置
        if Config.get_api_key():
            self.services_status["百炼-问答绘图服务"] = "已添加"

        # 检查通义听悟·会议纪要服务的App Key是否已配置
        if Config.get_app_key():
            self.services_status["通义听悟·会议纪要服务"] = "已添加"

# Run the application
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    settings_page = SettingsPage()
    settings_page.show()
    sys.exit(app.exec_())
