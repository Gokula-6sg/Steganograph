
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, 
    QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class SteganographyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = ""
        self.encrypted_image_path = "encrypted_image.png"  

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Steganography - PyQt5")
        self.setGeometry(100, 100, 600, 700)

        
        self.setStyleSheet("""
            QWidget { background-color: #2E3440; color: white; font-family: Arial; }
            QPushButton { background-color: #5E81AC; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #81A1C1; }
            QLineEdit { background-color: #4C566A; border-radius: 5px; padding: 6px; color: white; }
            QLabel { font-size: 14px; }
            QFrame { background-color: #4C566A; border-radius: 10px; }
        """)

      
        self.btn_select = QPushButton("📷 Select Image", self)
        self.btn_select.clicked.connect(self.select_image)

        
        self.image_frame = QFrame(self)
        self.image_label = QLabel("No Image Selected", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(300, 300)

        
        self.msg_label = QLabel("🔒 Enter Secret Message:")
        self.msg_entry = QLineEdit(self)

        self.pass_label = QLabel("🔑 Enter Passcode:")
        self.pass_entry = QLineEdit(self)
        self.pass_entry.setEchoMode(QLineEdit.Password)

        
        self.btn_encrypt = QPushButton("🛡 Encrypt Message", self)
        self.btn_encrypt.clicked.connect(self.encrypt_message)

        self.btn_decrypt = QPushButton("🔓 Decrypt Message", self)
        self.btn_decrypt.clicked.connect(self.decrypt_message)

        self.status_label = QLabel("", self)
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))

       
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_select)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.msg_label)
        vbox.addWidget(self.msg_entry)
        vbox.addWidget(self.pass_label)
        vbox.addWidget(self.pass_entry)
        vbox.addWidget(self.btn_encrypt)
        vbox.addWidget(self.btn_decrypt)
        vbox.addWidget(self.status_label)

        self.setLayout(vbox)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")

        if file_path:
            self.image_path = file_path
            self.img = cv2.imread(file_path)  
            pixmap = QPixmap(file_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.status_label.setText("✔ Image Loaded Successfully!")

    def encrypt_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please select an image first!")
            return

        msg = self.msg_entry.text()
        password = self.pass_entry.text()

        if not msg or not password:
            QMessageBox.warning(self, "Error", "Enter both message and password!")
            return

        img = cv2.imread(self.image_path)

        d = {chr(i): i for i in range(255)}
        n, m, z = 0, 0, 0

        for i in range(len(msg)):
            img[n, m, z] = d[msg[i]]
            n = (n + 1) % img.shape[0]
            m = (m + 1) % img.shape[1]
            z = (z + 1) % 3

        cv2.imwrite(self.encrypted_image_path, img)
        self.status_label.setText("🔐 Message Encrypted & Saved!")
        pixmap = QPixmap(self.encrypted_image_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def decrypt_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Please select an encrypted image first!")
            return

        input_pass = self.pass_entry.text()

        if not input_pass:
            QMessageBox.warning(self, "Error", "Enter passcode for decryption!")
            return

        encrypted_img = cv2.imread(self.encrypted_image_path)

        if encrypted_img is None:
            QMessageBox.warning(self, "Error", "Encrypted image not found!")
            return

        c = {i: chr(i) for i in range(255)}
        n, m, z = 0, 0, 0
        decrypted_msg = ""

        for i in range(len(self.msg_entry.text())):
            decrypted_msg += c[encrypted_img[n, m, z]]
            n = (n + 1) % encrypted_img.shape[0]
            m = (m + 1) % encrypted_img.shape[1]
            z = (z + 1) % 3

        QMessageBox.information(self, "Decryption", f"🔓 Decrypted Message: {decrypted_msg}")
        self.status_label.setText("✅ Message Decrypted!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SteganographyApp()
    win.show()
    sys.exit(app.exec_())
