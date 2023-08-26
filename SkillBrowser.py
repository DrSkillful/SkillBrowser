import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.create_navigation_toolbar()

        self.showMaximized()
        self.add_new_tab(QUrl('https://johnskillanimation.wixsite.com/skillbrowser'), 'homepage')
        self.setWindowTitle('SkillBrowser')

    def create_navigation_toolbar(self):
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        actions = [
            ('◀️', "Back to previous page", self.tabs.currentWidget().back),
            ('▶️', "Forward to next page", self.tabs.currentWidget().forward),
            ('🌀', "Reload page", self.tabs.currentWidget().reload),
            ('🏠', "Go home", self.navigate_home),
            ('Stop', "Stop loading current page", self.tabs.currentWidget().stop),
        ]

        for icon, tip, action in actions:
            action_btn = QAction(icon, self)
            action_btn.setStatusTip(tip)
            action_btn.triggered.connect(action)
            navtb.addAction(action_btn)

        navtb.addSeparator()

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlBar)

    def add_new_tab(self, qurl, label):
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda: self.update_title(browser))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab(QUrl('http://www.google.com'), 'New Tab')

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def update_title(self, browser):
        title = browser.page().title()
        self.setWindowTitle(f"{title} - SkillBrowser")

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlBar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser):
        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("SkillBrowser")
window = MainWindow()
app.exec_()
