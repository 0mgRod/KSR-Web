from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("KSR Web")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('assets', 'Logo256.png')))
        layout.addWidget(logo)

        build_number_path = "buildNumber.txt"

        # Read the current build number from the file
        with open(build_number_path, "r") as build_number_file:
            build_number_text = build_number_file.read().strip()

        # Convert the build number text to an integer
        build_number = int(build_number_text)
        layout.addWidget(QLabel("Build " + str(build_number)))
        layout.addWidget(QLabel("If you see that certain builds aren't published, this is because we also include test builds."))
        layout.addWidget(QLabel("Do not distribute any of KSR Web's source code as your own unless you want to risk facing legal issues."))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://ksr-industries.com/ksr-web/index"))

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)
        self.setUnifiedTitleAndToolBarOnMac(True)

        back_btn = QAction(QIcon(os.path.join('assets', 'BackArrow.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('assets', 'ForwardArrow')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('assets', 'Refresh.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('assets', 'Home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'HTTPS.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('assets', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('assets', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('assets', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('assets', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('assets', 'question.png')), "About KSR Web", self)
        about_action.setStatusTip("Find out more about KSR Web")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
        
        videos_menu = self.menuBar().addMenu("&KSR Videos")

        open_videos = QAction(QIcon(os.path.join('assets', 'disk--arrow.png')), "Open KSR Videos", self)
        open_videos.setStatusTip("Opens KSR Videos Website")  # Hungry!
        open_videos.triggered.connect(lambda: self.browser.setUrl(QUrl("http://ksr-industries.com/ksr-videos/index")))
        videos_menu.addAction(open_videos)

        open_videos = QAction(QIcon(os.path.join('assets', 'Upload.png')), "Upload", self)
        open_videos.setStatusTip("Uploads a Video of Your Choice")  # Hungry!
        open_videos.triggered.connect(lambda: self.browser.setUrl(QUrl("http://ksr-industries.com/ksr-videos/upload")))
        videos_menu.addAction(open_videos)
        
        launcher = self.menuBar().addMenu("&Omg Launcher")

        open_launcher = QAction(QIcon(os.path.join('assets', 'disk--arrow.png')), "Open Omg Launcher", self)
        open_launcher.setStatusTip("Opens Omg Launcher")  # Hungry!
        open_launcher.triggered.connect(lambda: self.browser.setUrl(QUrl("http://ksr-industries.com/omg/launcher.html")))
        launcher.addAction(open_launcher)

        navigate_mozarella_action = QAction(QIcon(os.path.join('assets', 'Home.png')), "KSR Web Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to KSR Web Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)

        self.show()


    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - KSR Web" % title)

    def navigate_mozarella(self):
        self.browser.setUrl(QUrl("http://www.ksr-industries.com"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.ksr-industries.com/ksr-web/index"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'HTTPS.png')))

        else:
            # Insecure padlock icon
            url = q.toString()
            if "ksr-industries.com" in url or "omg-chatz.atwebpages.com" in url:
                self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'HTTPS.png')))
            else:
                self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'HTTP.png')))
            self.urlbar.setText(url)

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QPushButton

    app = QApplication([])
    app.setStyleSheet("""
QWidget {
    background-color: #f5f5f5;
    font-size: 14px;
    font-family: Arial, sans-serif;
    color: #000;
}

QLabel {
    font-weight: bold;
}

QLineEdit {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 4px;
}

QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 4px 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #e0e0e0;
}

QPlainTextEdit {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 4px;
}

QScrollBar {
    width: 8px;
    background-color: #f5f5f5;
}

QScrollBar:vertical {
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #ddd;
    border: none;
    border-radius: 3px;
}

QScrollBar::add-line:vertical {
    border: none;
    background-color: #f5f5f5;
}

QScrollBar::sub-line:vertical {
    border: none;
    background-color: #f5f5f5;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background-color: #f5f5f5;
}

QStatusBar {
    background-color: #fff;
    border-top: 1px solid #ccc;
}

QToolBar {
    background-color: #f5f5f5;
    border-bottom: 1px solid #ccc;
    padding: 4px;
}

QToolButton {
    background-color: #f5f5f5;
    border: none;
    padding: 4px;
    margin-right: 4px;
}

QToolButton:hover {
    background-color: #e0e0e0;
}

    """)
    app.setApplicationName("KSR Web")
    app.setWindowIcon(QIcon(os.path.join('assets', 'KSRWeb.png')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

app.exec_()
