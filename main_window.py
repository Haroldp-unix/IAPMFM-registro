import os
import shutil
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QFormLayout, QLineEdit,
    QPushButton, QDateEdit, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox, QAbstractItemView, QComboBox
)
from PyQt5.QtCore import Qt, QDate, QDateTime, pyqtSignal
from PyQt5.QtGui import QPixmap

import database
from edit_dialog import EditDialog
from detalle_dialog import DetalleDialog


class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IAPMFM - Registro de Privados de Libertad")
        self.setMinimumSize(900, 600)
        self.init_ui()
        self.cargar_lista()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Pestaña Registro
        self.tab_registro = QWidget()
        self.tabs.addTab(self.tab_registro, "Registro")
        self.setup_registro_ui()

        # Pestaña Lista
        self.tab_lista = QWidget()
        self.tabs.addTab(self.tab_lista, "Lista de Reclusos")
        self.setup_lista_ui()

        # Barra de estado
        self.statusBar().showMessage("Sesión iniciada como admin")
        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.clicked.connect(self.emitir_logout)
        self.statusBar().addPermanentWidget(btn_logout)

    def emitir_logout(self):
        self.logout_signal.emit()

    def setup_registro_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        # --- Cédula con combo de nacionalidad ---
        cedula_layout = QHBoxLayout()
        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("12345678")
        self.cmb_nacionalidad = QComboBox()
        self.cmb_nacionalidad.addItems(["V", "E", "P"])
        self.cmb_nacionalidad.setFixedWidth(60)
        cedula_layout.addWidget(self.cmb_nacionalidad)
        cedula_layout.addWidget(self.txt_cedula)

        self.txt_apellidos = QLineEdit()
        self.txt_nombres = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate())
        self.txt_edad = QLineEdit()
        self.date_nacimiento.dateChanged.connect(self.calcular_edad)
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
        self.foto_path = ""

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
        btn_guardar = QPushButton("Guardar Recluso")
        btn_guardar.clicked.connect(self.guardar_recluso)
        layout.addWidget(btn_guardar)

        self.tab_registro.setLayout(layout)
        self.calcular_edad()

    def setup_lista_ui(self):
        layout = QVBoxLayout()
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Apellidos", "Nombres", "Cédula", "Fecha Registro"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.cellDoubleClicked.connect(self.mostrar_detalle)
        # Habilitar ordenación al hacer clic en los encabezados
        self.tabla.setSortingEnabled(True)
        layout.addWidget(self.tabla)

        btn_layout = QHBoxLayout()
        btn_ver = QPushButton("Ver Detalle")
        btn_ver.clicked.connect(self.ver_seleccionado)
        btn_editar = QPushButton("Modificar")
        btn_editar.clicked.connect(self.modificar_seleccionado)
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_seleccionado)
        btn_layout.addWidget(btn_ver)
        btn_layout.addWidget(btn_editar)
        btn_layout.addWidget(btn_eliminar)
        layout.addLayout(btn_layout)

        self.tab_lista.setLayout(layout)

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

    def guardar_recluso(self):
        letra = self.cmb_nacionalidad.currentText().strip()
        numero = self.txt_cedula.text().strip()
        cedula_completa = f"{letra}{numero}" if letra and numero else ""

        datos = {
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
        try:
            database.insertar_recluso(datos)
            QMessageBox.information(self, "Éxito", "Recluso registrado correctamente")
            self.limpiar_formulario()
            self.cargar_lista()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def limpiar_formulario(self):
        self.cmb_nacionalidad.setCurrentIndex(0)
        self.txt_cedula.clear()
        self.txt_apellidos.clear()
        self.txt_nombres.clear()
        self.date_nacimiento.setDate(QDate.currentDate())
        self.txt_natural.clear()
        self.txt_delito.clear()
        self.txt_tribunal.clear()
        self.txt_sentencia.clear()
        self.txt_pena.clear()
        self.txt_sala.clear()
        self.cmb_sangre.setCurrentIndex(0)
        self.lbl_foto.setText("No seleccionada")
        self.foto_path = ""

    def cargar_lista(self):
        # Desactivar ordenación mientras se llena para evitar parpadeos
        self.tabla.setSortingEnabled(False)
        self.tabla.setRowCount(0)
        reclusos = database.obtener_todos()
        for fila in reclusos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)

            # ID (numérico)
            item_id = QTableWidgetItem()
            item_id.setData(Qt.DisplayRole, int(fila[0]))
            self.tabla.setItem(row, 0, item_id)

            # Apellidos (texto)
            self.tabla.setItem(row, 1, QTableWidgetItem(fila[2]))

            # Nombres (texto)
            self.tabla.setItem(row, 2, QTableWidgetItem(fila[3]))

            # Cédula (texto)
            self.tabla.setItem(row, 3, QTableWidgetItem(fila[1]))

            # Fecha de registro (convertir a QDateTime para orden correcto)
            fecha_str = fila[14]  # "dd/MM/yyyy HH:mm:ss"
            item_fecha = QTableWidgetItem(fecha_str)
            fecha_dt = QDateTime.fromString(fecha_str, "dd/MM/yyyy HH:mm:ss")
            if fecha_dt.isValid():
                item_fecha.setData(Qt.DisplayRole, fecha_dt)
            self.tabla.setItem(row, 4, item_fecha)

        self.tabla.setSortingEnabled(True)

    def obtener_id_seleccionado(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Atención", "Seleccione un recluso de la lista")
            return None
        # Obtener el ID como entero desde el dato del item
        item = self.tabla.item(fila, 0)
        if item is None:
            return None
        return item.data(Qt.DisplayRole)

    def mostrar_detalle(self):
        self.ver_seleccionado()

    def ver_seleccionado(self):
        id_sel = self.obtener_id_seleccionado()
        if not id_sel:
            return
        datos = database.obtener_por_id(id_sel)
        if datos:
            dlg = DetalleDialog(datos, self)
            dlg.exec_()

    def modificar_seleccionado(self):
        id_sel = self.obtener_id_seleccionado()
        if not id_sel:
            return
        datos_actuales = database.obtener_por_id(id_sel)
        if not datos_actuales:
            return
        campos = ["id", "cedula", "apellidos", "nombres", "fecha_nacimiento",
                  "edad", "natural_de", "delito", "tribunal", "sentencia",
                  "pena_impuesta", "sala_resguardo", "tipo_sangre", "foto_path", "fecha_registro"]
        datos_dict = dict(zip(campos, datos_actuales))
        dlg = EditDialog(datos_dict, self)
        if dlg.exec_():
            nuevos = dlg.obtener_datos()
            database.actualizar_recluso(id_sel, nuevos)
            self.cargar_lista()
            QMessageBox.information(self, "Éxito", "Registro actualizado")

    def eliminar_seleccionado(self):
        id_sel = self.obtener_id_seleccionado()
        if not id_sel:
            return
        resp = QMessageBox.question(self, "Confirmar eliminación",
                                    "¿Está seguro de eliminar este registro?",
                                    QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            database.eliminar_recluso(id_sel)
            self.cargar_lista()
            QMessageBox.information(self, "Eliminado", "Registro eliminado")