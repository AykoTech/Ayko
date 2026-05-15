from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class JarvisSphere(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QUrl("assets/sphere.html"))
