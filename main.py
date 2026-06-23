import sys
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import database
from login_window import LoginWindow
from main_window import MainWindow

def cargar_estilo(app):
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        pass

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Importante para que no se cierre solo

    database.crear_tabla()
    cargar_estilo(app)

    # Splash
    splash_pix = QPixmap(400, 200)
    splash_pix.fill(Qt.black)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setFont(QFont("Arial", 14))
    splash.showMessage("Cargando sistema...", Qt.AlignCenter, Qt.white)
    splash.show()
    app.processEvents()
    time.sleep(1.5)
    splash.showMessage("Inicializando módulos...", Qt.AlignCenter, Qt.white)
    app.processEvents()
    time.sleep(0.8)
    splash.close()

    # Funciones anidadas para gestionar el ciclo login ↔ principal
    def mostrar_login():
        login = LoginWindow()
        if login.exec_() == QDialog.Accepted:
            main_win = MainWindow()
            # Conectamos la señal de cierre de sesión para volver al login
            main_win.logout_signal.connect(lambda: cerrar_sesion(main_win))
            main_win.show()
        else:
            app.quit()  # Salir si cancela el login

    def cerrar_sesion(ventana):
        ventana.close()
        mostrar_login()  # Vuelve a pedir credenciales

    mostrar_login()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()