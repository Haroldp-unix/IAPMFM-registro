from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from datetime import datetime
import locale

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    pass

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acceso al Sistema")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        lbl_justicia = QLabel("JUSTICIA")
        lbl_justicia.setAlignment(Qt.AlignCenter)
        lbl_justicia.setStyleSheet("font-size: 32px; font-weight: bold; color: #CCCCCC;")
        layout.addWidget(lbl_justicia)

        # Subtítulo
        lbl_iapmfm = QLabel("IAPMFM")
        lbl_iapmfm.setAlignment(Qt.AlignCenter)
        lbl_iapmfm.setStyleSheet("font-size: 18px; color: #AAAAAA; margin-bottom: 20px;")
        layout.addWidget(lbl_iapmfm)

        # Campos de usuario y contraseña
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Usuario")
        self.txt_usuario.setStyleSheet("padding: 8px;")
        layout.addWidget(self.txt_usuario)

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Contraseña")
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setStyleSheet("padding: 8px;")
        layout.addWidget(self.txt_password)

        # Botón ingresar
        btn_ingresar = QPushButton("Ingresar")
        btn_ingresar.clicked.connect(self.verificar_login)
        layout.addWidget(btn_ingresar)

        # Pie de página: "Calabozo, mes y año en curso"
        mes_actual = datetime.now().strftime("%B").capitalize()
        año_actual = datetime.now().year
        lbl_pie = QLabel(f"Calabozo, {mes_actual} {año_actual}")
        lbl_pie.setAlignment(Qt.AlignCenter)
        lbl_pie.setStyleSheet("color: #888888; margin-top: 20px;")
        layout.addWidget(lbl_pie)

        self.setLayout(layout)

    def verificar_login(self):
        if self.txt_usuario.text() == "admin" and self.txt_password.text() == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")