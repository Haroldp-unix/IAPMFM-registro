from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton,
                             QFileDialog, QLabel, QVBoxLayout, QHBoxLayout,
                             QDateEdit, QComboBox)
from PyQt5.QtCore import QDate
import os
import shutil
from datetime import datetime

class EditDialog(QDialog):
    def __init__(self, datos=None, parent=None):
        super().__init__(parent)
        self.datos_originales = datos
        self.foto_path = datos["foto_path"] if datos else ""
        self.setWindowTitle("Modificar Recluso" if datos else "Nuevo Recluso")
        self.setMinimumWidth(450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # Cédula con nacionalidad
        cedula_layout = QHBoxLayout()
        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("12345678")
        self.cmb_nacionalidad = QComboBox()
        self.cmb_nacionalidad.addItems(["V", "E", "P"])
        cedula_layout.addWidget(self.cmb_nacionalidad)
        cedula_layout.addWidget(self.txt_cedula)

        # Separar la cédula completa en letra y número si vienen datos
        if self.datos_originales and self.datos_originales.get("cedula"):
            cedula = self.datos_originales["cedula"]
            if len(cedula) > 1 and cedula[0].isalpha():
                letra = cedula[0]
                num = cedula[1:]
                idx = self.cmb_nacionalidad.findText(letra)
                if idx >= 0:
                    self.cmb_nacionalidad.setCurrentIndex(idx)
                self.txt_cedula.setText(num)
            else:
                self.txt_cedula.setText(cedula)

        self.txt_apellidos = QLineEdit()
        self.txt_nombres = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.txt_edad = QLineEdit()
        self.txt_natural = QLineEdit()
        self.txt_delito = QLineEdit()
        self.txt_tribunal = QLineEdit()
        self.txt_sentencia = QLineEdit()
        self.txt_pena = QLineEdit()
        self.txt_pena.setPlaceholderText("12 años")
        self.txt_sala = QLineEdit()
        self.cmb_sangre = QComboBox()
        self.cmb_sangre.addItems(["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.lbl_foto = QLabel("No seleccionada")

        # Rellenar si hay datos
        if self.datos_originales:
            self.txt_apellidos.setText(self.datos_originales.get("apellidos", ""))
            self.txt_nombres.setText(self.datos_originales.get("nombres", ""))
            fec = self.datos_originales.get("fecha_nacimiento", "")
            if fec:
                self.date_nacimiento.setDate(QDate.fromString(fec, "dd/MM/yyyy"))
            self.txt_edad.setText(str(self.datos_originales.get("edad", "")))
            self.txt_natural.setText(self.datos_originales.get("natural_de", ""))
            self.txt_delito.setText(self.datos_originales.get("delito", ""))
            self.txt_tribunal.setText(self.datos_originales.get("tribunal", ""))
            self.txt_sentencia.setText(self.datos_originales.get("sentencia", ""))
            self.txt_pena.setText(self.datos_originales.get("pena_impuesta", ""))
            self.txt_sala.setText(self.datos_originales.get("sala_resguardo", ""))
            sangre = self.datos_originales.get("tipo_sangre", "")
            idx = self.cmb_sangre.findText(sangre)
            if idx >= 0:
                self.cmb_sangre.setCurrentIndex(idx)
            if self.foto_path:
                self.lbl_foto.setText(os.path.basename(self.foto_path))
        else:
            self.date_nacimiento.setDate(QDate.currentDate())

        self.date_nacimiento.dateChanged.connect(self.calcular_edad)

        form.addRow("Cédula:", cedula_layout)
        form.addRow("Apellidos:", self.txt_apellidos)
        form.addRow("Nombres:", self.txt_nombres)
        form.addRow("Fecha de Nacimiento:", self.date_nacimiento)
        form.addRow("Edad:", self.txt_edad)
        form.addRow("Natural de:", self.txt_natural)
        form.addRow("Delito:", self.txt_delito)
        form.addRow("Tribunal:", self.txt_tribunal)
        form.addRow("Sentencia:", self.txt_sentencia)
        form.addRow("Pena impuesta:", self.txt_pena)
        form.addRow("Sala de resguardo:", self.txt_sala)
        form.addRow("Tipo de sangre:", self.cmb_sangre)

        foto_layout = QHBoxLayout()
        btn_foto = QPushButton("Seleccionar foto")
        btn_foto.clicked.connect(self.seleccionar_foto)
        foto_layout.addWidget(btn_foto)
        foto_layout.addWidget(self.lbl_foto)
        form.addRow("Foto:", foto_layout)

        layout.addLayout(form)
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.accept)
        layout.addWidget(btn_guardar)

        self.setLayout(layout)
        self.calcular_edad()

    def calcular_edad(self):
        fecha = self.date_nacimiento.date().toPyDate()
        hoy = datetime.now().date()
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        self.txt_edad.setText(str(edad))

    def seleccionar_foto(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar foto", "",
                                                 "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if archivo:
            os.makedirs("fotos", exist_ok=True)
            nombre_unico = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{os.path.basename(archivo)}"
            destino = os.path.join("fotos", nombre_unico)
            shutil.copy2(archivo, destino)
            self.foto_path = destino
            self.lbl_foto.setText(nombre_unico)

    def obtener_datos(self):
        letra = self.cmb_nacionalidad.currentText().strip()
        numero = self.txt_cedula.text().strip()
        cedula_completa = f"{letra}{numero}" if letra and numero else ""
        return {
            "cedula": cedula_completa,
            "apellidos": self.txt_apellidos.text().strip(),
            "nombres": self.txt_nombres.text().strip(),
            "fecha_nacimiento": self.date_nacimiento.date().toString("dd/MM/yyyy"),
            "edad": int(self.txt_edad.text()) if self.txt_edad.text().isdigit() else 0,
            "natural_de": self.txt_natural.text().strip(),
            "delito": self.txt_delito.text().strip(),
            "tribunal": self.txt_tribunal.text().strip(),
            "sentencia": self.txt_sentencia.text().strip(),
            "pena_impuesta": self.txt_pena.text().strip(),
            "sala_resguardo": self.txt_sala.text().strip(),
            "tipo_sangre": self.cmb_sangre.currentText(),
            "foto_path": self.foto_path
        }