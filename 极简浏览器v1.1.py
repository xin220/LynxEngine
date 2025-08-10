import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                            QLineEdit, QAction, QVBoxLayout, QWidget, QStatusBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LynxEngine")
        self.setGeometry(100, 100, 1024, 768)
        
        # 设置窗口图标（可选）
        try:
            self.setWindowIcon(QIcon("browser_icon.png"))
        except:
            pass
        
        # 创建浏览器视图
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.baidu.com"))
        
        # 创建导航栏
        navbar = QToolBar("导航栏")
        navbar.setMovable(False)
        self.addToolBar(navbar)
        
        # 后退按钮
        back_btn = QAction("←", self)
        back_btn.setToolTip("后退")
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)
        
        # 前进按钮
        forward_btn = QAction("→", self)
        forward_btn.setToolTip("前进")
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)
        
        # 刷新按钮
        reload_btn = QAction("↻", self)
        reload_btn.setToolTip("刷新")
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)
        
        # 停止按钮
        stop_btn = QAction("✕", self)
        stop_btn.setToolTip("停止加载")
        stop_btn.triggered.connect(self.browser.stop)
        navbar.addAction(stop_btn)
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.setPlaceholderText("输入网址...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        # 主页按钮
        home_btn = QAction("🏠", self)
        home_btn.setToolTip("主页")
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        
        # 连接URL变化信号
        self.browser.urlChanged.connect(self.update_url)
        
        # 连接加载进度信号
        self.browser.loadProgress.connect(self.update_progress)
        
        # 连接标题变化信号
        self.browser.titleChanged.connect(self.update_title)
        
        # 连接加载状态变化信号
        self.browser.loadStarted.connect(self.page_loading_started)
        self.browser.loadFinished.connect(self.page_loading_finished)
        
        # 设置中央部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(navbar)
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 加载进度变量
        self.progress_value = 0
        
        # 设置主页（可配置）
        self.home_url = "https://www.baidu.com"
        
        # 设置初始URL
        self.browser.setUrl(QUrl(self.home_url))
    
    def navigate_to_url(self):
        """导航到地址栏中的URL"""
        url = self.url_bar.text().strip()
        if not url:
            return
            
        try:
            # 自动添加协议前缀
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
                
            self.browser.setUrl(QUrl(url))
            
        except Exception as e:
            self.status_bar.showMessage(f"错误: {str(e)}", 3000)
    
    def navigate_home(self):
        """导航到主页"""
        self.browser.setUrl(QUrl(self.home_url))
    
    def update_url(self, q):
        """更新地址栏显示"""
        self.url_bar.setText(q.toString())
        self.url_bar.selectAll()  # 自动选择所有文本方便修改
        self.status_bar.showMessage(f"已加载: {q.toString()}", 3000)
    
    def update_progress(self, progress):
        """更新加载进度"""
        self.progress_value = progress
        self.status_bar.showMessage(f"加载中... {progress}%")
    
    def update_title(self, title):
        """更新窗口标题"""
        self.setWindowTitle(f"{title} - 极简浏览器")
    
    def page_loading_started(self):
        """页面开始加载"""
        self.status_bar.showMessage("加载中... 0%")
    
    def page_loading_finished(self, success):
        """页面加载完成"""
        if success:
            self.status_bar.showMessage(f"加载完成 {self.progress_value}%", 2000)
        else:
            self.status_bar.showMessage("页面加载失败", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式（可选）
    app.setStyle("Fusion")
    
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
