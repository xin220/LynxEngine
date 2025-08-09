import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                            QLineEdit, QAction, QVBoxLayout, QWidget)
from PyQt5.QtWebEngineWidgets import QWebEngineView  # 确保已安装PyQtWebEngine

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("极简浏览器")
        self.setGeometry(100, 100, 1024, 768)
        
        # 创建浏览器视图
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.baidu.com"))
        
        # 创建导航栏
        navbar = QToolBar()
        self.addToolBar(navbar)
        
        # 后退按钮
        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)
        
        # 前进按钮
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)
        
        # 刷新按钮
        reload_btn = QAction("↻", self)  # 修复：使用单个刷新符号
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # 主页按钮
        home_btn = QAction("🏠", self)  # 修复：使用单个主页符号
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        # 连接URL变化信号
        self.browser.urlChanged.connect(self.update_url)
        
        # 设置中央部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(navbar)
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))
    
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.baidu.com"))
    
    def update_url(self, q):
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
