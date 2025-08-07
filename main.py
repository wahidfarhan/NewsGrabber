import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox
from newsWindow import Ui_Form
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QBuffer
from PyQt5.QtGui import QColor, QBrush
import requests
from bs4 import BeautifulSoup
import webbrowser
from reader import scrape_jugantor_news
# post_thread.py

from PyQt5.QtCore import QThread, pyqtSignal
import requests

class PostThread(QThread):
    finished = pyqtSignal(bool, str)  # success, message

    def __init__(self, page_id, access_token, message, image_bytes):
        super().__init__()
        self.page_id = page_id
        self.access_token = access_token
        self.message = message
        self.image_bytes = image_bytes

    def run(self):
        try:
            # Upload photo to Facebook
            photo_url = f"https://graph.facebook.com/v18.0/{self.page_id}/photos"
            payload = {
                'access_token': self.access_token,
                'message': self.message,
            }
            files = {
                'source': ('image.jpg', self.image_bytes, 'image/jpeg')
            }

            response = requests.post(photo_url, data=payload, files=files)
            data = response.json()

            if response.status_code == 200 and "id" in data:
                self.finished.emit(True, "Posted successfully!")
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error occurred')
                self.finished.emit(False, f"Failed to post: {error_msg}")
        except Exception as e:
            self.finished.emit(False, str(e))

class NewsFetcherThread(QThread):
    news_fetched = pyqtSignal(str, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            for item in soup.select('.thumbnail'):
                title_tag = item.find(['h1', 'h3'])
                link_tag = item.find('a', href=True)
                if title_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    link = link_tag['href']
                    results.append((title, link))

            for item in soup.select('.media'):
                title_tag = item.find(['h4', 'h3'])
                link_tag = item.find('a', href=True)
                if title_tag and link_tag:
                    title = title_tag.get_text(strip=True)
                    link = link_tag['href']
                    results.append((title, link))

            for title, link in results:
                news, imageslinks = scrape_jugantor_news(link)
                self.news_fetched.emit(title, link)

        except Exception as e:
            self.news_fetched.emit(f"Error fetching news: {str(e)}", "")

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.serial = 1
        self.thread = None

        # Connect button click — use lambda to pass the URL
        self.ui.National.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/national"))
        self.ui.Latest.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/latest"))
        self.ui.Political.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/politics"))
        self.ui.Country.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/country-news"))
        self.ui.Education.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/campus"))
        self.ui.Corporate.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/corporate-news"))
        self.ui.Islam.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/islam"))
        self.ui.Various.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/various"))
        self.ui.Socialmedia.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/social-media"))
        self.ui.Interview.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/interview"))
        self.ui.Litareture.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/literature"))
        self.ui.Jobs.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/job-seek"))
        self.ui.International.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/international"))
        self.ui.Technology.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/tech"))
        self.ui.Others.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/bicchu"))
        self.ui.LifeStyle.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/lifestyle"))
        self.ui.Entertainment.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/entertainment"))
        self.ui.Economics.clicked.connect(lambda: self.on_category_clicked("https://www.jugantor.com/economics"))
        self.ui.BackButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.PostButton.clicked.connect(self.postFun)
        # Connect double click to open link
        self.ui.listWidget.itemDoubleClicked.connect(self.open_news_link)

    def on_category_clicked(self, url):
        if url.startswith("https://www.jugantor.com/"):
            stripped = url[len("https://www.jugantor.com/"):]
            print(stripped)  # Output: economics
        self.ui.Tittle_Load_Label.setText(stripped.capitalize())
        self.ui.listWidget.clear()
        self.serial = 1
        self.start_fetch(url)

    def start_fetch(self, url):
        if self.thread and self.thread.isRunning():
            return

        self.thread = NewsFetcherThread(url)
        self.thread.news_fetched.connect(self.add_news_item)
        self.thread.start()

    def add_news_item(self, title, link):
        item_text = f"{self.serial}. {title}"
        item = QtWidgets.QListWidgetItem(item_text)
        item.setBackground(QBrush(QColor("#f0f0f0")))
        item.setForeground(QBrush(QColor("#000000")))
        item.setFont(QtGui.QFont("Arial", 10))
        item.setData(QtCore.Qt.UserRole, link)

        self.ui.listWidget.addItem(item)
        self.serial += 1

    import re

    # ধরুন self.ui.imageLabel একটি QLabel, সেটির সেটআপ Qt Designer এ করুন

    # ধরুন self.ui.imageLabel একটি QLabel, সেটির সেটআপ Qt Designer এ করুন

    def open_news_link(self, item):
        import re
        link = item.data(QtCore.Qt.UserRole)
        if link:
            self.ui.textEdit.setHtml("<h3>Loading...</h3>")  # Loading মেসেজ HTML ফরম্যাটে
            self.ui.stackedWidget.setCurrentIndex(1)

            news_text, image_urls = scrape_jugantor_news(link)

            # আরও পড়ুন repetitive অংশ ও URL লাইন ক্লিন করুন
            news_text = re.sub(r'(আরও পড়ুন)+', 'আরও পড়ুন', news_text)
            news_text = re.sub(r'URL:\s*https?://\S+', '', news_text).strip()

            # শিরোনাম: item.text() থেকে সিরিয়াল নম্বর বাদ দিয়ে শুধু টাইটেল অংশ নিন
            # যেমন: "1. Some Title" থেকে "Some Title"
            import re
            raw_title = item.text()
            title_only = re.sub(r'^\d+\.\s*', '', raw_title)

            # QTextEdit এ HTML সেট করুন, h1 ট্যাগে টাইটেল, তারপর প্যারাগ্রাফে খবরের অংশ
            html_content = f"<h1>{title_only}</h1><p style='font-size:12pt; line-height:1.4;'>{news_text}</p>"
            self.ui.textEdit.setHtml(html_content)

            # ছবি দেখানোর জন্য
            if image_urls:
                from PyQt5.QtGui import QPixmap
                import requests
                clean_url = image_urls[0].replace("url:", "").strip()
                try:
                    response = requests.get(clean_url)
                    image = QPixmap()
                    image.loadFromData(response.content)
                    self.ui.imageLabel.setPixmap(image.scaledToWidth(400, QtCore.Qt.SmoothTransformation))
                except Exception as e:
                    print("Image load failed:", e)
                    self.ui.imageLabel.clear()
            else:
                self.ui.imageLabel.clear()

    def postFun(self):
        # Get the message from textEdit
        message = self.ui.textEdit.toPlainText()

        # Get pixmap from imageLabel
        pixmap = self.ui.imageLabel.pixmap()
        if not pixmap:
            QMessageBox.critical(self, "Error", "No image to post.")
            return

        # Convert pixmap to bytes
        buffer = QBuffer()
        buffer.open(QBuffer.WriteOnly)
        pixmap.save(buffer, "PNG")
        image_bytes = buffer.data()

        # Start post thread
        self.post_thread = PostThread(
            page_id="599649106574283",
            access_token="EAAabmyMcwzYBPEg6NdUQaBENleZBf5ATfDaMAXgRVk66L1CryYNCNMFtdvbDZCKjelQHYEzyKnMDZBOJsprOCHhjLpale0oTG8n6RwY0KPjfjMf2CSFTnQ5tNqpu1oqTUbcYpsEulzPP9FKhjaXuzXKSkMZCmJhPBQ5sngmQhyc2m2OCPDdXbNcvjHoIZBDtZCYVRUdkCcpbqfLNCr1QuwKVr6ccT0uDs9cLyf2O0D",
            message=message,
            image_bytes=image_bytes
        )
        self.post_thread.finished.connect(self.on_post_finished)
        self.post_thread.start()

    def on_post_finished(self, success, message):
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)

    def on_post_success(self, message):
        QMessageBox.information(self, "Success", message)

    def on_post_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec_())
