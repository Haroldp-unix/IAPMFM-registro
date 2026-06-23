from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter
import os

class DetalleDialog(QDialog):
    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.datos = datos
        self.setWindowTitle("Detalle del Recluso")
        self.setMinimumWidth(450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ID (solo en pantalla)
        lbl_id = QLabel(f"<b>ID:</b>  {self.datos[0]}")
        lbl_id.setTextFormat(Qt.RichText)
        layout.addWidget(lbl_id)

        # Filiación del Penado
        lbl_filiacion = QLabel("<b><u>Filiación del Penado:</u></b>")
        lbl_filiacion.setTextFormat(Qt.RichText)
        layout.addWidget(lbl_filiacion)

        # Campos
        info = [
            ("Cédula", self.datos[1]),
            ("Apellidos", self.datos[2]),
            ("Nombres", self.datos[3]),
            ("Fecha de Nacimiento", self.datos[4]),
            ("Edad", str(self.datos[5])),
            ("Natural de", self.datos[6]),
            ("Delito", self.datos[7]),
            ("Tribunal", self.datos[8]),
            ("Sentencia", self.datos[9]),
            ("Pena impuesta", self.datos[10]),
            ("Sala de resguardo", self.datos[11]),
            ("Tipo de sangre", self.datos[12]),
            ("Fecha de registro", self.datos[14])
        ]

        for etiqueta, valor in info:
            lbl = QLabel(f"<b>{etiqueta}:</b>  {valor}")
            lbl.setTextFormat(Qt.RichText)
            layout.addWidget(lbl)

        # Foto y botones
        bottom_layout = QHBoxLayout()
        foto_layout = QVBoxLayout()
        lbl_foto = QLabel()
        if self.datos[13] and os.path.exists(self.datos[13]):
            pixmap = QPixmap(self.datos[13])
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(180, Qt.SmoothTransformation)
                lbl_foto.setPixmap(pixmap)
        else:
            lbl_foto.setText("Sin foto")
        lbl_foto.setAlignment(Qt.AlignCenter)
        foto_layout.addWidget(lbl_foto)

        btn_pdf = QPushButton("Imprimir / Guardar PDF")
        btn_pdf.clicked.connect(self.generar_pdf)
        foto_layout.addWidget(btn_pdf)
        bottom_layout.addLayout(foto_layout)

        bottom_layout.addStretch()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        bottom_layout.addWidget(btn_cerrar)

        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def generar_pdf(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", "", "Archivos PDF (*.pdf)")
        if not ruta:
            return
        try:
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(ruta)
            printer.setPageSize(QPrinter.A4)

            painter = QPainter()
            if not painter.begin(printer):
                QMessageBox.critical(self, "Error", "No se pudo iniciar la impresión PDF")
                return

            # Configurar fuentes
            font_normal = QFont("Arial", 12)
            font_bold = QFont("Arial", 12)
            font_bold.setBold(True)

            y = 100
            x = 100

            # Filiación del Penado
            painter.setFont(font_bold)
            painter.drawText(x, y, "Filiación del Penado:")
            y += 30

            # Campos a imprimir
            campos = [
                ("Cédula", self.datos[1]),
                ("Apellidos", self.datos[2]),
                ("Nombres", self.datos[3]),
                ("Fecha de Nacimiento", self.datos[4]),
                ("Edad", str(self.datos[5])),
                ("Natural de", self.datos[6]),
                ("Delito", self.datos[7]),
                ("Tribunal", self.datos[8]),
                ("Sentencia", self.datos[9]),
                ("Pena impuesta", self.datos[10]),
                ("Sala de resguardo", self.datos[11]),
                ("Tipo de sangre", self.datos[12])
            ]

            for etiqueta, valor in campos:
                painter.setFont(font_bold)
                painter.drawText(x, y, f"{etiqueta}: ")
                # Calcular ancho del texto para continuar después
                ancho_etiqueta = painter.fontMetrics().boundingRect(f"{etiqueta}:  ").width()
                painter.setFont(font_normal)
                # Se añaden píxeles de separación extra
                painter.drawText(x + ancho_etiqueta + 2, y, str(valor))
                y += 25

            # Foto si existe
            if self.datos[13] and os.path.exists(self.datos[13]):
                pixmap = QPixmap(self.datos[13])
                if not pixmap.isNull():
                    pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)
                    painter.drawPixmap(x, y + 10, pixmap)

            painter.end()
            QMessageBox.information(self, "PDF generado", f"Se guardó correctamente en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el PDF:\n{e}")