import sys
import urllib.parse
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, 
                            QLineEdit, QAction, QVBoxLayout, QWidget, 
                            QStatusBar, QToolButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LynxEngine")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置现代UI风格
        self.setup_ui_style()
        
        # 创建浏览器视图
        self.browser = QWebEngineView()
        
        # 创建紧凑导航栏（包含地址栏）
        self.create_compact_navbar()
        
        # 连接信号与槽
        self.connect_signals()
        
        # 设置中央部件
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.navbar)
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setFont(QFont("Arial", 8))  # 减小状态栏字体
        self.status_bar.showMessage("Ready")
        
        # 设置主页
        self.home_url = "https://www.baidu.com"
        self.browser.setUrl(QUrl(self.home_url))
        
        # 加载进度变量
        self.progress_value = 0
        # 初始化更新导航按钮状态
        self.update_navigation_buttons()
    
    def setup_ui_style(self):
        """设置现代UI风格"""
        # 设置应用样式
        app = QApplication.instance()
        app.setStyle("Fusion")
        
        # 创建调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(76, 163, 224))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)
    
    def create_compact_navbar(self):
        """创建极致紧凑导航栏（单行整合地址栏）"""
        self.navbar = QToolBar("Navigation Bar")
        self.navbar.setMovable(False)
        self.navbar.setIconSize(QSize(16, 16))  # 小图标尺寸
        
        # 后退按钮
        self.back_btn = QAction(QIcon.fromTheme("go-previous"), "", self)
        self.back_btn.setToolTip("Back")
        self.back_btn.triggered.connect(self.browser.back)
        self.navbar.addAction(self.back_btn)
        
        # 前进按钮
        self.forward_btn = QAction(QIcon.fromTheme("go-next"), "", self)
        self.forward_btn.setToolTip("Forward")
        self.forward_btn.triggered.connect(self.browser.forward)
        self.navbar.addAction(self.forward_btn)
        
        # 刷新按钮
        self.reload_btn = QAction(QIcon.fromTheme("view-refresh"), "", self)
        self.reload_btn.setToolTip("Refresh")
        self.reload_btn.triggered.connect(self.browser.reload)
        self.navbar.addAction(self.reload_btn)
        
        # 停止按钮
        self.stop_btn = QAction(QIcon.fromTheme("process-stop"), "", self)
        self.stop_btn.setToolTip("Stop")
        self.stop_btn.triggered.connect(self.browser.stop)
        self.navbar.addAction(self.stop_btn)
        
        # 书签按钮
        self.bookmark_btn = QToolButton()
        self.bookmark_btn.setText("★")
        self.bookmark_btn.setToolTip("Add Bookmark")
        self.bookmark_btn.setFixedSize(18, 18)  # 最小化尺寸
        self.bookmark_btn.clicked.connect(self.toggle_bookmark)
        self.navbar.addWidget(self.bookmark_btn)
        
        # 地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.setPlaceholderText("Enter URL or search...")
        self.url_bar.setFont(QFont("Arial", 8))  # 更小字体
        self.url_bar.setMinimumHeight(18)  # 最小高度
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)
        
        # Go按钮
        self.go_btn = QToolButton()
        self.go_btn.setText("Go")
        self.go_btn.setFont(QFont("Arial", 8))  # 最小字体
        self.go_btn.setFixedSize(30, 18)  # 更小尺寸
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.navbar.addWidget(self.go_btn)
        
        # 主页按钮
        self.home_btn = QAction(QIcon.fromTheme("go-home"), "", self)
        self.home_btn.setToolTip("Home")
        self.home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(self.home_btn)
        
        # 设置导航栏样式
        self.navbar.setStyleSheet("""
            QToolBar {
                background-color: #f0f0f0;
                border-bottom: 1px solid #d0d0d0;
                padding: 1px;
            }
            QToolButton {
                border: none;
                padding: 1px;
                margin: 0 1px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-radius: 2px;
            }
            QLineEdit {
                border: 1px solid #c0c0c0;
                border-radius: 2px;
                padding: 1px 3px;
                font-size: 8pt;
                min-height: 18px;
            }
        """)
    
    def connect_signals(self):
        """连接信号与槽"""
        # 连接URL变化信号
        self.browser.urlChanged.connect(self.update_url)
        
        # 连接加载进度信号
        self.browser.loadProgress.connect(self.update_progress)
        
        # 连接标题变化信号
        self.browser.titleChanged.connect(self.update_title)
        
        # 连接加载状态变化信号
        self.browser.loadStarted.connect(self.page_loading_started)
        self.browser.loadFinished.connect(self.page_loading_finished)
        
        # 连接导航状态变化信号
        self.browser.urlChanged.connect(self.update_navigation_buttons)
        self.browser.loadFinished.connect(self.update_navigation_buttons)
    
    def update_navigation_buttons(self):
        """更新后退和前进按钮状态"""
        history = self.browser.history()
        self.back_btn.setEnabled(history.canGoBack())
        self.forward_btn.setEnabled(history.canGoForward())
    
    def navigate_to_url(self):
        """智能导航到地址栏中的URL"""
        url_text = self.url_bar.text().strip()
        if not url_text:
            return
            
        try:
            # 智能URL处理
            if self.is_valid_url(url_text):
                url = url_text
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
            else:
                # 如果不是URL，则进行搜索
                url = f"https://www.baidu.com/s?wd={urllib.parse.quote(url_text)}"
                
            self.browser.setUrl(QUrl(url))
            
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}", 3000)
    
    def is_valid_url(self, text):
        """检查文本是否是有效的URL"""
        # 简单检查URL的有效性
        return '.' in text and ' ' not in text and not text.startswith('?')
    
    def navigate_home(self):
        """导航到主页"""
        self.browser.setUrl(QUrl(self.home_url))
    
    def update_url(self, q):
        """更新地址栏显示"""
        url_str = q.toString()
        self.url_bar.setText(url_str)
        self.url_bar.selectAll()
        
        # 更新书签状态
        self.update_bookmark_state(url_str)
        
        # 状态栏消息
        if len(url_str) > 50:
            display_url = url_str[:20] + "..." + url_str[-30:]
        else:
            display_url = url_str
        self.status_bar.showMessage(f"Loaded: {display_url}", 3000)
    
    def update_bookmark_state(self, url):
        """更新书签按钮状态"""
        # 这里只是一个示例，实际应用中需要维护书签列表
        if "baidu" in url:
            self.bookmark_btn.setStyleSheet("color: gold; font-weight: bold;")
            self.bookmark_btn.setToolTip("Bookmarked (click to remove)")
        else:
            self.bookmark_btn.setStyleSheet("")
            self.bookmark_btn.setToolTip("Add Bookmark")
    
    def toggle_bookmark(self):
        """切换书签状态"""
        current_url = self.url_bar.text()
        if "baidu" in current_url:  # 模拟书签状态
            self.bookmark_btn.setStyleSheet("")
            self.bookmark_btn.setToolTip("Add Bookmark")
            self.status_bar.showMessage("Removed from bookmarks", 2000)
        else:
            self.bookmark_btn.setStyleSheet("color: gold; font-weight: bold;")
            self.bookmark_btn.setToolTip("Bookmarked (click to remove)")
            self.status_bar.showMessage("Added to bookmarks", 2000)
    
    def update_progress(self, progress):
        """更新加载进度"""
        self.progress_value = progress
        self.status_bar.showMessage(f"Loading... {progress}%")
        
        # 动态更新停止按钮状态
        self.stop_btn.setEnabled(progress < 100)
    
    def update_title(self, title):
        """更新窗口标题"""
        if len(title) > 50:
            title = title[:50] + "..."
        self.setWindowTitle(f"{title} - LynxEngine")
    
    def page_loading_started(self):
        """页面开始加载"""
        self.status_bar.showMessage("Loading... 0%")
        self.reload_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def page_loading_finished(self, success):
        """页面加载完成"""
        self.reload_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            self.status_bar.showMessage(f"Load complete", 2000)
        else:
            self.status_bar.showMessage("Page load failed", 3000)
            
        # 确保导航按钮状态更新
        self.update_navigation_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用字体
    font = QFont("Microsoft YaHei UI", 8)  # 更小字体
    app.setFont(font)
    
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
