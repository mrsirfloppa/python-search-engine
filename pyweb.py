import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget,
                             QTabWidget, QPushButton, QHBoxLayout, QShortcut, QStyleFactory, QLabel)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.navigate_to_url)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.navigate_to_url)

        self.image_search_button = QPushButton("Image Search")
        self.image_search_button.clicked.connect(self.navigate_to_image_search)

        self.video_search_button = QPushButton("Video Search")
        self.video_search_button.clicked.connect(self.navigate_to_video_search)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.search_bar)
        toolbar_layout.addWidget(self.search_button)
        toolbar_layout.addWidget(self.image_search_button)
        toolbar_layout.addWidget(self.video_search_button)

        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def navigate_to_url(self):
        url = self.search_bar.text()
        if not url.startswith("http"):
            url = f"https://www.google.com/search?q={url}"
        self.browser.setUrl(QUrl(url))

    def navigate_to_image_search(self):
        query = self.search_bar.text()
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        self.browser.setUrl(QUrl(url))

    def navigate_to_video_search(self):
        query = self.search_bar.text()
        url = f"https://duckduckgo.com/?q={query}&iax=videos&ia=videos"
        self.browser.setUrl(QUrl(url))

class SimpleWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.add_new_tab(QUrl("http://google.com"))
        self.setCentralWidget(self.tabs)

        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)

    def add_new_tab(self, url=None):
        if url is None:
            url = QUrl("http://google.com")

        new_tab = BrowserTab()
        new_tab.browser.setUrl(url)
        new_tab.search_bar.setText(url.toString())  # Convert QUrl to string
        new_tab.browser.urlChanged.connect(lambda new_url: new_tab.search_bar.setText(new_url.toString()))

        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    browser = SimpleWebBrowser()
    browser.show()

    sys.exit(app.exec_())
