import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget,
                             QTabWidget, QPushButton, QHBoxLayout, QShortcut)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.update_url)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter URL and press Enter')
        self.url_input.returnPressed.connect(self.load_url)

        layout.addWidget(self.url_input)
        layout.addWidget(self.browser)

        self.setLayout(layout)

        if url:
            self.browser.setUrl(url)
        else:
            self.browser.setUrl(QUrl("https://www.google.com"))

    def load_url(self):
        url = QUrl.fromUserInput(self.url_input.text())
        self.browser.setUrl(url)

    def update_url(self, url):
        self.url_input.setText(url.toString())

class SimpleWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.add_new_tab(QUrl("https://www.google.com"))

        self.addTabButton = QPushButton("+")
        self.addTabButton.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(self.addTabButton)

        layout.addWidget(self.tabs)

        # Add keyboard shortcuts
        self.new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.new_tab_shortcut.activated.connect(self.add_new_tab)
        self.close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_tab_shortcut.activated.connect(self.close_current_tab)
        self.full_screen_shortcut = QShortcut(QKeySequence("F11"), self)
        self.full_screen_shortcut.activated.connect(self.toggle_full_screen)

    def add_new_tab(self, url=None):
        new_tab = BrowserTab(url=url)
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        tab_to_close = self.tabs.widget(index)
        tab_to_close.deleteLater()
        self.tabs.removeTab(index)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        self.close_tab(current_index)

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

global app

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = SimpleWebBrowser()
    browser.show()
    sys.exit(app.exec_())
