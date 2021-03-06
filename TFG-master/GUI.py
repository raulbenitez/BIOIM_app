from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QScreen
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QApplication, QTableWidget, QTableWidgetItem
import pyautogui
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from segmentada import Segmentada
import matplotlib.image as mpimg
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(Qt.transparent))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)

        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)


class Ui_TFG(QMainWindow, Segmentada):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segmentada = Segmentada() #heredamos de segmentada
        self.imageLabel = PhotoViewer(self)
        self.imageLabel_2 = PhotoViewer(self)

    def setupUi(self, TFG):
        TFG.setObjectName("TFG")
        TFG.resize(1366, 768)
        TFG.setMinimumSize(QtCore.QSize(1366, 760))
        TFG.setAutoFillBackground(False)
        TFG.setStyleSheet("background-image: url('dddef.jpg');\n"
"font: 75 14pt \"Segoe UI\";\n"
"\n"
"Qframe\n"
"{\n"
"background:#333\n"
"border-radius:60px\n"
"}")

        self.centralwidget = QtWidgets.QWidget(TFG)
        self.centralwidget.setObjectName("centralwidget")

        self.taula = QtWidgets.QTableWidget(self.centralwidget)
        self.taula.setGeometry(QtCore.QRect(30, 60, 311, 571))
        self.taula.setAutoFillBackground(True)
        self.taula.verticalHeader().setVisible(False)
        self.taula.setObjectName("taula")
        
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 10, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("\n"
"QFrame\n"
"{\n"
"background:#008c00;\n"
"border-radius:15px;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"color:white;\n"
"}")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(890, 10, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("\n"
"QFrame\n"
"{\n"
"background:#333;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"color:white;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(380, 10, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("\n"
"QFrame\n"
"{\n"
"background:#333;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"color:white;\n"
"}")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")

        pg.setConfigOption('foreground', 'w')
        self.histogram = PlotWidget(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(380, 450, 651, 211))
        self.histogram.setObjectName("histogram")
        self.histogram.setBackground((30, 30, 30))



        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(380, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("\n"
"QFrame\n"
"{\n"
"background:#333;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"color:white;\n"
"}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.printer = QPrinter()
        self.scaleFactor = 0.0
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(380, 60, 451, 321))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(True)

        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(890, 60, 451, 321))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setWidget(self.imageLabel_2)
        self.scrollArea_2.setVisible(True)

#####################
#      BUTTONS

        self.clickbutt = QtWidgets.QPushButton(self.centralwidget)
        self.clickbutt.setGeometry(QtCore.QRect(650, 30, 101, 21))
        self.clickbutt.setStyleSheet("font: 10pt \"Lucida Sans Unicode\";\n"
"background: rgb(255, 0, 0);\n"
"border-radius:5px;\n"
"color:white;")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("mouse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clickbutt.setIcon(icon9)
        self.clickbutt.setObjectName("clickbutt")

###     BOTONES DE IMAGEN PROCESADA

        self.clickbutt_2 = QtWidgets.QPushButton(self.centralwidget)
        self.clickbutt_2.setGeometry(QtCore.QRect(1160, 30, 101, 21))
        self.clickbutt_2.setStyleSheet("font: 10pt \"Lucida Sans Unicode\";\n"
"background: rgb(255, 0, 0);\n"
"border-radius:5px;\n"
"color:white;")
        self.clickbutt_2.setIcon(icon9)
        self.clickbutt_2.setObjectName("clickbutt_2")

##### OTHER BUTTONS

        self.trashbutt = QtWidgets.QPushButton(self.centralwidget)
        self.trashbutt.setGeometry(QtCore.QRect(1290, 390, 51, 31))
        self.trashbutt.setStyleSheet("font: 10pt \"Lucida Sans Unicode\";\n"
"background:#333;\n"
"border-radius:5px;\n"
"color:white;")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trashbutt.setIcon(icon10)
        self.trashbutt.setIconSize(QtCore.QSize(20, 20))
        self.trashbutt.setObjectName("trashbutt")

        self.guardar_tabla = QtWidgets.QPushButton(self.centralwidget)
        self.guardar_tabla.setGeometry(QtCore.QRect(30, 640, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.guardar_tabla.setFont(font)
        self.guardar_tabla.setAutoFillBackground(False)
        self.guardar_tabla.setStyleSheet("font: 10pt \"Lucida Sans Unicode\";\n"
"background: #008c00;\n"
"border-radius:5px;\n"
"color:white;")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("guardar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.guardar_tabla.setIcon(icon11)
        self.guardar_tabla.setObjectName("guardar_tabla")

#       END BUTTONS
#       LABELfont

        self.co_1 = QtWidgets.QLabel(self.centralwidget)
        self.co_1.setGeometry(QtCore.QRect(760, 30, 71, 21))

        self.co_1.setAlignment(QtCore.Qt.AlignCenter)
        self.co_1.setStyleSheet("font: 75 10pt \"Segoe UI\";\n")
        self.co_1.setObjectName("co_1")

        self.co_2 = QtWidgets.QLabel(self.centralwidget)
        self.co_2.setGeometry(QtCore.QRect(1270, 30, 71, 21))

        self.co_2.setAlignment(QtCore.Qt.AlignCenter)
        self.co_2.setStyleSheet("font: 75 10pt \"Segoe UI\";\n")
        self.co_2.setObjectName("co_2")

##########################################

        TFG.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TFG)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 31))
        self.menubar.setObjectName("menubar")
       
    
        self.createAction() 
        self.createMenus()

    def open(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QImage(fileName) #necesitamos una QImage para hacer el display en qpixmap

            self.img_op = mpimg.imread(fileName) # pero para editar la imagen es mejor convertirla a un numpy array. Así pues,
            #será "self.img" la que pasaremos para las segmentaciones y filtros.

            if image.isNull():
                QMessageBox.information(self, "Image imageLabel", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPhoto(QtGui.QPixmap(image))

            self.process = None


            #   ENABLE the actions that need an image
            self.printAct.setEnabled(True)

            self.actionOtsu.setEnabled(True)
            self.actionWatershed.setEnabled(True)
            self.actionQuikshift.setEnabled(True)
            self.actionFelzenszwalb.setEnabled(True)
            self.actioncontrast_log.setEnabled(True)
            self.actionContrast_gamma.setEnabled(True)
            self.actionAutom_tic.setEnabled(True)
            self.actionk_manual.setEnabled(True)
            self.actionHistograma.setEnabled(True)


            if len(self.img_op.shape) ==2:
                self.actionGrayscale.setEnabled(True)
            elif len(self.img_op.shape) == 3 or len(self.img_op.shape) == 4:
                self.actionRGB.setEnabled(True)
                self.actionGrayscale.setEnabled(True)


    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def shoot(self):
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
        p = QScreen.grabWindow(app.primaryScreen(), self.centralwidget.winId()).save(filename, 'png')
        mu = QMessageBox()

        if self.actionCatal.isChecked():
            mu.setText("Imatge: '" + filename + "' guardada correctament")
        if self.actionCastellano.isChecked():
            mu.setText("Imagen: '" + filename + "' guardada correctamente")
        if self.actionEnglish.isChecked():
            mu.setText("Image: '" + filename + "' has been saved successfully")    

        mu.setWindowTitle("Warning")
        mu.setIcon(QMessageBox.Information)
        x = mu.exec_()


    def pixInfo(self):
        self.imageLabel.toggleDragMode()

    def photoClicked(self, pos):
        if self.imageLabel.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.co_1.setText('%d, %d' % (pos.x(), pos.y()))

    def pixInfo2(self):
        self.imageLabel_2.toggleDragMode()

    def photoClicked2(self, pos):
        if self.imageLabel_2.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.co_2.setText('%d, %d' % (pos.x(), pos.y()))
        

    def guardar(self):
        date = datetime.now()
        filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
        p = QScreen.grabWindow(app.primaryScreen(), self.scrollArea_2.winId()).save(filename, 'png')
        mx = QMessageBox()

        if self.actionCatal.isChecked():
            mx.setText("Imatge: '" + filename + "' guardada correctament")
        if self.actionCastellano.isChecked():
            mx.setText("Imagen: '" + filename + "' guardada correctamente")
        if self.actionEnglish.isChecked():
            mx.setText("Image: '" + filename + "' has been saved successfully")    

        mx.setWindowTitle("Warning")
        mx.setIcon(QMessageBox.Information)
        x = mx.exec_()


    def about_aim(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("OBJECTIU DE L'APLICACIÓ")
            m.setText("<p> L'aplicació té l'objectiu de proporcionar una "
                        "llibreria d'aplicacions de processament d'imatges biomèdiques amb entorn gràfic d'usuari,"
                        " gràcies al desenvolupament d'un conjunt d'eines de processament d'imatges biomèdiques. </p>"
                        "<p> Les eines inclouen algorismes de pre-processat, filtratge, detecció de contorns,"
                        " anàlisi de textura i segmentació d'objectes. L'eina està orientada a un ús en entorns"
                        " de recerca clínica i aplicacions de suport al diagnòstic.</p>")

        if self.actionCastellano.isChecked():
            m.setWindowTitle("OBJECTIVO DE LA APLICACIÓN")
            m.setText("<p> El programa tiene el objectivo de proporcionar una "
                        "libreria de aplicaciones de procesamiento de imágenes biomédicas con un entorno gráfico de usuario,"
                        " gracias al desarrollo de un conjunto de herramientas de procesamiento de imágenes biomédicas. </p>"
                        "<p> Las herramientas incluyen algoritmos de pre-procesado, filtrado, detección de contornos,"
                        " análisis de textura y segmentación de objetos. La herramienta está orientada a un uso en entornos"
                        " de investigación clínica y aplicaciones de apoyo al diagnóstico.</p>")

        if self.actionEnglish.isChecked():
            m.setWindowTitle("APPICATION'S AIM")
            m.setText("<p> The application aims to provide a "
                        "biomedical image processing library with graphical user environment (GUI), through"
                        " the development of a set of biomedical image processing tools. </p>"
                        "<p> The tools include pre-processing algorithms, filtering, contour detection,"
                        " texture analysis and object segmentation. The tool is use-oriented in "
                        " clinical research environments and diagnostic support applications.</p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()

    def about_gmm(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("GAUSSIAN MIXTURE MODEL")
            m.setText("<p> En aquesta aplicació s'han implementat dos tipus de segmentació GMM; "
                        "per imatges grayscale i per imatges en RGB. </p>"
                        "<p> Si la imatge original té format RGB podrà fer tant segmentació GMM-Grayscale"
                        " com segmentació GMM-RGB. Però, en cas d'escollir una imatge original en escala de grisos"
                        ", només es podrà dur a terme la segmentació GMM-grayscale.</p>")

        if self.actionCastellano.isChecked():
            m.setWindowTitle("GAUSSIAN MIXTURE MODEL")
            m.setText("<p> En esta aplicación se han implementado dos tipos de segmentación GMM; "
                        "para imágenes grayscale y para imágenes en RGB. </p>"
                        "<p> Si la imagen original tiene formato RGB podrá hacer tanto segmentación GMM-Grayscale"
                        " como segmentación GMM-RGB. Pero, en caso de elegir una imagen original en escala de grises"
                        ", sólo se podrá llevar a cabo la segmentación GMM-grayscale.</p>")

        if self.actionEnglish.isChecked():
            m.setWindowTitle("GAUSSIAN MIXTURE MODEL")
            m.setText("<p> Two types of GMM segmentation have been implemented in this application; "
                        "for grayscale images and RGB images. </p>"
                        "<p> If the original image has RGB format both GMM-Grayscale segmentation"
                        " and GMM-RGB segmentation can be chosen. Akin, in case of a grayscale original image"
                        ", only GMM-grayscale segmentation will be allowed.</p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()


    def about_contrast(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("SEGMENTACIÓ I CONTRAST")
            m.setText("<p> En el moment de fer la segmentació, l'aplicació tindrà en compte si s'ha fet"
                        " un contrast previament a la imatge. En cas de ser així, la segmentació es farà sobre"
                        " la imatge amb el contrast. </p>"
                        "<p> En cas de voler eliminar el contrast per dur a terme la segmentació, "
                        "cliqui sobre el botó de l'escombraria i, posteriorment, segmenti la imatge.</p>")

        if self.actionCastellano.isChecked():
            m.setWindowTitle("SEGMENTACIÓN I CONTRASTE")
            m.setText("<p> En el momento de hacer la segmentación, la aplicación tendrá en cuenta si se ha hecho"
                        " un contraste previamente a la imagen. En caso afirmativo, la segmentación se hará sobre"
                        " la imagen con contraste. </p>"
                        "<p> En caso de querer eliminar el contraste para llevar a cabo la segmentación, "
                        "clique sobre el botón de la basura y, posteriormente, segmente la imagen.</p>")

        if self.actionEnglish.isChecked():
            m.setWindowTitle("SEGMENTATION & CONTRAST")
            m.setText("<p> When segmenting the image, the app considers whether it has been applied a contrast"
                        " previously. If so, the segmentation will be done to"
                        " the filtered image. </p>"
                        "<p> In case you wish to remove the contrast to perform the segmentation "
                        "click on the rubbish button and then segment the image.</p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()

    def about_table(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("TAULA DE CARACTERÍSTIQUES")
            m.setText("<p> Les característiques extretes s'obtenen a partir de la funció 'regionprops' de Python."
                        " S'aplicarà aquesta funció sobre la última imatge processada, amb la segmentació corresponent. </p>"
                        "<p> En cas de voler veure les característiques amb una segmentació diferent,"
                        " segmenti altre cop la imatge i després actualitzi la taula.</p>")


        if self.actionCastellano.isChecked():
            m.setWindowTitle("TABLA DE CARACTERÍSTICAS")
            m.setText("<p> Las características extraídas se obtienen a partir de la función 'regionprops' de Python."
                        " Se aplicará esta función sobre la última imagen procesada, con la segmentación correspondiente. </p>"
                        "<p> En caso de querer ver las características con una segmentación diferente,"
                        " segmente de nuevo la imagen y luego actualice la tabla.</p>")


        if self.actionEnglish.isChecked():
            m.setWindowTitle("FEATURES TABLE")
            m.setText("<p> The extracted features are obtained from Python's 'regionprops' function."
                        " This function will be applied to the last image processed, with the corresponding segmentation. </p>"
                        "<p> In case you wish to see the characteristics with a different segmentation,"
                        " segment the image again and then update the table.</p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()

    def about_habilitar(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("PAN / (X, Y)")
            m.setText("<p> Aquesta opció permet, quan està habilitada, moure la imatge a la finestra."
                        " En cas contrari, mostra les coordenades del píxel al clicar sobre la imatge. </p>"
                        "<p> Per passar d'un mode a l'altre simplement cliqui sobre el botó vermell.</p>")

        if self.actionCastellano.isChecked():
            m.setWindowTitle("PAN / (X, Y)")
            m.setText("<p> Esta opción permite, cuando está habilitada, mover la imagen en la ventana."
                        " En caso contrario, muestra las coordenadas del píxel al clicar sobre la imagen. </p>"
                        "<p> Para pasar de un modo a otro simplemente pulse sobre el botón rojo.</p>")

        if self.actionEnglish.isChecked():
            m.setWindowTitle("ENABLING")
            m.setText("<p> This option allows, when enabled, to move the image throughout the window"
                        " When it is not enabled, it shows the pixel coordinates when clicking on the image."
                        " To switch from one mode to another simply click on the red button. </p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()

    def about_save(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("GUARDAR IMATGES I CAPTURES DE PANTALLA")
            m.setText("<p> Les imatges i les captures de pantalla es guardaran amb el nom de la data i l'hora"
                        " del moment en que s'ha fet. Trobarà les imatges a la mateixa carpeta on tingui"
                        " l'aplicació. </p>")


        if self.actionCastellano.isChecked():
            m.setWindowTitle("GUARDAR IMÁGENES Y CAPTURAS DE PANTALLA")
            m.setText("<p> Las imágenes y las capturas de pantalla se guardarán con el nombre de la fecha y la hora"
                        " del momento en que se han hecho. Encontrará las imágenes en la misma carpeta donde tenga"
                        " la aplicación. </p>")


        if self.actionEnglish.isChecked():
            m.setWindowTitle("SAVE IMAGES & SCREENSHOTS")
            m.setText("<p> The images and screenshots will be saved with the name of the date and time"
                        " of the moment when they have been taken. You will find the images in the same folder where you have "
                        "the application. </p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()

    def about_hist_gauss(self):
        m = QMessageBox()
        if self.actionCatal.isChecked():
            m.setWindowTitle("HISTOGRAMA AMB GAUSSIANES")
            m.setText("<p> Mostra l'histograma en grayscale de la imatge original i les gaussianes que s'han"
                        " trobat amb la segmentació GMM. A la llegenda s'indica la mitja i la covariància de cadascuna. </p>"
                        "<p> Opció només disponible per segmentació GMM-grayscale.</p>")


        if self.actionCastellano.isChecked():
            m.setWindowTitle("HISTOGRAMA CON GAUSIANAS")
            m.setText("<p> Muestra el histograma en grayscale de la imagen original y las gausianas que se han"
                        " encontrado con la segmentación GMM. En la leyenda se indica la media y la covarianza decada una. </p>"
                        "<p> Opción únicamente disponible para segmentación GMM-grayscale.</p>")


        if self.actionEnglish.isChecked():
            m.setWindowTitle("HISTOGRAM WITH GAUSSIAN CURVES")
            m.setText("<p> Displays the grayscale histogram of the original image and the Gaussian curves"
                        " found by the GMM segmentation. The legend indicates the mean and the covariance of each of them. </p>"
                        "<p> Only available for GMM-grayscale segmentation.</p>")

        m.setIcon(QMessageBox.Information)
        y = m.exec_()


    def conceptes(self):
        m = QMessageBox()
        
        if self.actionCatal.isChecked():
            m.setWindowTitle("CONCEPTES")
            m.setText("<p> Cliqui sobre els conceptes següents per saber més informació: </p>" 
                        "<p> <a href=\"https://www.python.org/\"  >Python</a>" "</p>"
                        "<p> <a href=\"https://doc.qt.io/qtforpython/\"  >PyQt5</a>" "</p>"
                        "<p> <a href=\"https://daedalus.umkc.edu/StatisticalMethods/histograms.html\"  >Histogram</a>" "</p>"
                        "<p> <a href=\"https://micro.magnet.fsu.edu/primer/java/digitalimaging/processing/gamma/index.html\"  >Contrast</a>" "</p>"
                        "<p> <a href=\"https://www.upf.edu/web/simbiosys/segmentation\"  >Segmentation</a>" "</p>"
                        "<p> <a href=\"https://scikit-learn.org/stable/modules/mixture.html#gmm\"  >Gaussian Mixture Model (GMM) </a>" "</p>")
        
        if self.actionCastellano.isChecked():
            m.setWindowTitle("CONCEPTOS")
            m.setText("<p> Clique sobre los conceptos siguientes para saber más información: </p>" 
                        "<p> <a href=\"https://www.python.org/\"  >Python</a>" "</p>"
                        "<p> <a href=\"https://doc.qt.io/qtforpython/\"  >PyQt5</a>" "</p>"
                        "<p> <a href=\"https://daedalus.umkc.edu/StatisticalMethods/histograms.html\"  >Histogram</a>" "</p>"
                        "<p> <a href=\"https://micro.magnet.fsu.edu/primer/java/digitalimaging/processing/gamma/index.html\"  >Contrast</a>" "</p>"
                        "<p> <a href=\"https://www.upf.edu/web/simbiosys/segmentation\"  >Segmentation</a>" "</p>"
                        "<p> <a href=\"https://scikit-learn.org/stable/modules/mixture.html#gmm\"  >Gaussian Mixture Model (GMM) </a>" "</p>")
        

        if self.actionEnglish.isChecked():
            m.setWindowTitle("CONCEPTS")
            m.setText("<p> Click on the links below for further information: </p>" 
                        "<p> <a href=\"https://www.python.org/\"  >Python</a>" "</p>"
                        "<p> <a href=\"https://doc.qt.io/qtforpython/\"  >PyQt5</a>" "</p>"
                        "<p> <a href=\"https://daedalus.umkc.edu/StatisticalMethods/histograms.html\"  >Histogram</a>" "</p>"
                        "<p> <a href=\"https://micro.magnet.fsu.edu/primer/java/digitalimaging/processing/gamma/index.html\"  >Contrast</a>" "</p>"
                        "<p> <a href=\"https://www.upf.edu/web/simbiosys/segmentation\"  >Segmentation</a>" "</p>"
                        "<p> <a href=\"https://scikit-learn.org/stable/modules/mixture.html#gmm\"  >Gaussian Mixture Model (GMM) </a>" "</p>")
        

        m.setIcon(QMessageBox.Information)
        y = m.exec_()
#################################
    def createAction(self):
        self.actionSeleccionar_imatge = QtWidgets.QAction(TFG)
        self.actionSeleccionar_imatge.triggered.connect(self.open)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSeleccionar_imatge.setIcon(icon)
        self.actionSeleccionar_imatge.setObjectName("actionSeleccionar_imatge")


        self.actionGuardar = QtWidgets.QAction(self, shortcut="Ctrl+S", triggered=self.guardar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("guardar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGuardar.setIcon(icon1)
        self.actionGuardar.setObjectName("actionGuardar")

        self.actionScreenshot = QtWidgets.QAction(self, shortcut="Ctrl+G", triggered=self.shoot)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("scshot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionScreenshot.setIcon(icon1)
        self.actionScreenshot.setObjectName("actionScreenshot")

        self.actionHistograma = QtWidgets.QAction("&Histograma", self, enabled=False, triggered=self.histograma)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("plot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHistograma.setIcon(icon2)
        self.actionHistograma.setObjectName("actionHistograma")

        self.actionHistograma_amb_Gaussianes = QtWidgets.QAction(self, enabled=False, triggered=self.hist_gauss)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("gmm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHistograma_amb_Gaussianes.setIcon(icon3)
        self.actionHistograma_amb_Gaussianes.setObjectName("actionHistograma_amb_Gaussianes")

        self.actionContrast_gamma = QtWidgets.QAction("&Gamma", self, enabled=False, triggered=self.gammacorrection)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("gamma.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionContrast_gamma.setIcon(icon4)
        self.actionContrast_gamma.setObjectName("actionContrast_gamma")

        self.actioncontrast_log = QtWidgets.QAction("&Logarítmic", self, enabled=False, triggered=self.logcorrection)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("log.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncontrast_log.setIcon(icon5)
        self.actioncontrast_log.setObjectName("actioncontrast_log")

        self.action_rea_Intensitat = QtWidgets.QAction("&Àrea/Intensitat", self, enabled=False, triggered=self.scatter)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("graph.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rea_Intensitat.setIcon(icon6)
        self.action_rea_Intensitat.setObjectName("action_rea_Intensitat")

        self.actionOtsu = QtWidgets.QAction("&Otsu", self, enabled=False, triggered=self.segm_otsu)
        self.actionOtsu.setObjectName("actionOtsu")

        self.actionWatershed = QtWidgets.QAction("&Watershed", self, enabled=False, triggered=self.segm_water)
        self.actionWatershed.setObjectName("actionWatershed")

        self.actionAutom_tic = QtWidgets.QAction("&Automàtic", self, enabled=False, triggered=self.segm_k)
        self.actionAutom_tic.setObjectName("actionAutom_tic")

        self.actionFelzenszwalb = QtWidgets.QAction("&Felzenszwalb", self, enabled=False, triggered=self.segm_felz)
        self.actionFelzenszwalb.setObjectName("actionFelzenszwalb")

        self.actionQuikshift = QtWidgets.QAction("&Quickshift", self, enabled=False, triggered=self.segm_quick)
        self.actionQuikshift.setObjectName("actionQuikshift")

        self.actionGrayscale = QtWidgets.QAction("&Imatge Grayscale", self, enabled=False, triggered=self.segmentacio_gauss_g)
        self.actionGrayscale.setObjectName("actionGrayscale")

        self.actionRGB = QtWidgets.QAction("&Imatge RGB", self, enabled=False, triggered=self.segmentacio_gauss_color)
        self.actionRGB.setObjectName("actionRGB")

        self.actionk_manual = QtWidgets.QAction("&Manual", self, enabled=False, triggered=self.manual)
        self.actionk_manual.setObjectName("actionk_manual")


        self.actionPropietats = QtWidgets.QAction(self, enabled=False, triggered=self.prop)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap("table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPropietats.setIcon(icon20)
        self.actionPropietats.setObjectName("actionPropietats")
        
        self.clickbutt.clicked.connect(self.pixInfo)
        self.imageLabel.photoClicked.connect(self.photoClicked)


        self.clickbutt_2.clicked.connect(self.pixInfo2)
        self.imageLabel_2.photoClicked.connect(self.photoClicked2)

        self.guardar_tabla.clicked.connect(self.handleSave)
        self.guardar_tabla.setEnabled(False)

        self.printAct = QtWidgets.QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printAct.setIcon(icon7)
        self.printAct.setObjectName("printAct")

        self.about_aim_Act  = QAction(self, triggered=self.about_aim)
        self.aboutQtAct = QAction("&Qt", self, triggered=qApp.aboutQt)

        self.about_gmm_act  = QAction(self, triggered=self.about_gmm)

        self.about_contrast_act  = QAction(self, triggered=self.about_contrast)

        self.about_table_act  = QAction(self, triggered=self.about_table)

        self.about_habilitar_act  = QAction(self, triggered=self.about_habilitar)

        self.about_save_act  = QAction(self, triggered=self.about_save)
        self.about_hist_gauss_act =  QAction(self, triggered=self.about_hist_gauss)



        self.actionCatal = QtWidgets.QAction(self, checkable=True, triggered=self.retranslateUi)
        self.actionCatal.setChecked(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("cat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCatal.setIcon(icon11)
        self.actionCatal.setObjectName("actionCatal")

        self.actionCastellano = QtWidgets.QAction(self,checkable=True, triggered=self.idioma_castellano)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("spain.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCastellano.setIcon(icon12)
        self.actionCastellano.setObjectName("actionCastellano")
        self.actionEnglish = QtWidgets.QAction(self,checkable=True, triggered=self.idioma_english)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("eng.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEnglish.setIcon(icon13)
        self.actionEnglish.setObjectName("actionEnglish")

        self.trashbutt.clicked.connect(self.delete_process)
        if self.actionCatal.isChecked():
            self.trashbutt.setToolTip('Eliminar contrast')
        
        self.conceptes_act = QtWidgets.QAction(self, triggered=self.conceptes)

    def createMenus(self):
        self.menuFitxer = QtWidgets.QMenu(self.menubar)
        self.menuFitxer.setObjectName("menuFitxer")
        self.menuFitxer.addAction(self.actionSeleccionar_imatge)
        self.menuFitxer.addAction(self.actionGuardar)
        self.menuFitxer.addAction(self.printAct)
        self.menuFitxer.addAction(self.actionScreenshot)


        self.menuHistograma = QtWidgets.QMenu(self.menubar)
        self.menuHistograma.setObjectName("menuHistograma")
        self.menuHistograma.addAction(self.actionHistograma)
        self.menuHistograma.addAction(self.actionHistograma_amb_Gaussianes)

        self.menuProcessament = QtWidgets.QMenu(self.menubar)
        self.menuProcessament.setObjectName("menuProcessament")
        self.menuProcessament.addAction(self.actionContrast_gamma)
        self.menuProcessament.addAction(self.actioncontrast_log)


        self.menuSegmentaci = QtWidgets.QMenu(self.menubar)
        self.menuSegmentaci.setObjectName("menuSegmentaci")
        self.menuSegmentaci.addAction(self.actionOtsu)
        self.menuSegmentaci.addAction(self.actionWatershed)
        self.menuSegmentaci.addAction(self.actionFelzenszwalb)
        self.menuSegmentaci.addAction(self.actionQuikshift)

        self.menuK_Means = QtWidgets.QMenu(self.menuSegmentaci)
        self.menuSegmentaci.addAction(self.menuK_Means.menuAction())

        self.menuGMM = QtWidgets.QMenu(self.menuSegmentaci)
        self.menuSegmentaci.addAction(self.menuGMM.menuAction())

        self.menuK_Means.setObjectName("menuK_Means")
        self.menuK_Means.addAction(self.actionAutom_tic)
        self.menuK_Means.addAction(self.actionk_manual)



        self.menuGMM.setObjectName("menuGMM")
        self.menuGMM.addAction(self.actionGrayscale)
        self.menuGMM.addAction(self.actionRGB)

        self.menuPropietats = QtWidgets.QMenu(self.menubar)
        self.menuPropietats.setObjectName("menuPropietats")
        self.menuPropietats.addAction(self.actionPropietats)
        if self.actionCatal.isChecked():
            self.menuPropietats.setToolTip('Sobre la última segmentació realitzada')
        

        self.menuGr_fic = QtWidgets.QMenu(self.menubar)
        self.menuGr_fic.setObjectName("menuGr_fic")
        self.menuGr_fic.addAction(self.action_rea_Intensitat)



        self.menuIdioma = QtWidgets.QMenu(self.menubar)
        self.menuIdioma.setObjectName("menuIdioma")
        self.menuIdioma.addAction(self.actionCatal)
        self.menuIdioma.addAction(self.actionCastellano)
        self.menuIdioma.addAction(self.actionEnglish)

        self.menuAjuda = QtWidgets.QMenu(self.menubar)
        self.menuAjuda.setObjectName("menuAjuda")
        self.menuAjuda.addAction(self.aboutQtAct)
        self.menuAjuda.addAction(self.conceptes_act)

        self.MenuAbout = QtWidgets.QMenu(self.menuAjuda)
        self.menuAjuda.addAction(self.MenuAbout.menuAction())
        self.MenuAbout.addAction(self.about_aim_Act)
        self.MenuAbout.addAction(self.about_gmm_act)
        self.MenuAbout.addAction(self.about_contrast_act)
        self.MenuAbout.addAction(self.about_table_act)
        self.MenuAbout.addAction(self.about_habilitar_act)
        self.MenuAbout.addAction(self.about_save_act)
        self.MenuAbout.addAction(self.about_hist_gauss_act)

        self.menubar.addAction(self.menuFitxer.menuAction())

        self.menubar.addAction(self.menuHistograma.menuAction())
        self.menubar.addAction(self.menuProcessament.menuAction())
        self.menubar.addAction(self.menuSegmentaci.menuAction())
        self.menubar.addAction(self.menuPropietats.menuAction())
        self.menubar.addAction(self.menuGr_fic.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())
        self.menubar.addAction(self.menuIdioma.menuAction())



        TFG.setMenuBar(self.menubar)
        self.retranslateUi(TFG)
        QtCore.QMetaObject.connectSlotsByName(TFG)
        _translate = QtCore.QCoreApplication.translate
        TFG.setWindowTitle(_translate("TFG", "TFG"))
        self.actionCatal.setChecked(True)
        self.actionCastellano.setChecked(False)
        self.actionEnglish.setChecked(False)

    def retranslateUi(self, TFG):
        self.actionCatal.setChecked(True)
        self.actionCastellano.setChecked(False)
        self.actionEnglish.setChecked(False)

        self.trashbutt.setToolTip('Eliminar contrast')
        self.menuPropietats.setToolTip('Sobre la última segmentació realitzada')

        _translate = QtCore.QCoreApplication.translate
        self.about_hist_gauss_act.setText(_translate("TFG", "Histograma amb Gaussianes"))
        self.conceptes_act.setText(_translate("TFG", "Conceptes"))
        self.about_aim_Act.setText(_translate("TFG", "Objectiu"))
        self.about_gmm_act.setText(_translate("TFG", "GMM"))
        self.about_contrast_act.setText(_translate("TFG", "Contrast"))
        self.about_table_act.setText(_translate("TFG", "Taula de característiques"))
        self.about_habilitar_act.setText(_translate("TFG", "Pan / zoom"))
        self.about_save_act.setText(_translate("TFG", "Guardar imatges"))
        self.MenuAbout.setTitle(_translate("TFG", "L'aplicació"))
        self.label_8.setText(_translate("TFG", "Taula de característiques"))
        self.label_2.setText(_translate("TFG", "Imatge Processada"))
        self.label_1.setText(_translate("TFG", "Imatge Original"))
        self.label_5.setText(_translate("TFG", "Histograma"))
       
        self.clickbutt.setText(_translate("TFG", "Pan / (x , y)"))
        self.clickbutt_2.setText(_translate("TFG", "Pan / (x , y)"))
        
        self.guardar_tabla.setText(_translate("TFG", "Guardar dades"))
        self.co_1.setText('(x , y)')
        self.co_2.setText('(x , y)')
        self.menuFitxer.setTitle(_translate("TFG", "Fitxer"))

        self.menuHistograma.setTitle(_translate("TFG", "Histograma"))
        self.menuProcessament.setTitle(_translate("TFG", "Contrast"))
        self.menuSegmentaci.setTitle(_translate("TFG", "Segmentació"))
        self.menuK_Means.setTitle(_translate("TFG", "K-Means"))
        self.actionk_manual.setText(_translate("TFG", "Manual"))
        self.menuGMM.setTitle(_translate("TFG", "GMM"))
        self.menuPropietats.setTitle(_translate("TFG", "Propietats"))

        self.menuGr_fic.setTitle(_translate("TFG", "Gràfic"))
        self.menuAjuda.setTitle(_translate("TFG", "Ajuda"))
        self.clickbutt.setShortcut(_translate("TFG", "Ctrl+M"))
        self.clickbutt_2.setShortcut(_translate("TFG", "Ctrl+O"))
        self.menuIdioma.setTitle(_translate("TFG", "Idioma"))
        self.actionSeleccionar_imatge.setText(_translate("TFG", "Seleccionar imatge"))
        self.actionSeleccionar_imatge.setShortcut(_translate("TFG", "Ctrl+F"))
        self.actionGuardar.setText(_translate("TFG", "Guardar imatge processada"))
        self.actionGuardar.setShortcut(_translate("TFG", "Ctrl+S"))
        self.actionScreenshot.setText(_translate("TFG", "Captura de pantalla"))
        self.actionHistograma.setText(_translate("TFG", "Histograma"))
        self.actionHistograma_amb_Gaussianes.setText(_translate("TFG", "Histograma amb Gaussianes"))
        self.actionContrast_gamma.setText(_translate("TFG", "Gamma"))
        self.actioncontrast_log.setText(_translate("TFG", "Logarítmic"))
        self.action_rea_Intensitat.setText(_translate("TFG", "Àrea / Intensitat"))
        self.actionOtsu.setText(_translate("TFG", "Otsu"))
        self.actionWatershed.setText(_translate("TFG", "Watershed"))
        self.actionAutom_tic.setText(_translate("TFG", "Automàtic"))
        self.actionFelzenszwalb.setText(_translate("TFG", "Felzenszwalb"))
        self.actionQuikshift.setText(_translate("TFG", "Quikshift"))
        self.actionGrayscale.setText(_translate("TFG", "Grayscale"))
        self.actionRGB.setText(_translate("TFG", "RGB"))
        self.actionPropietats.setText(_translate("TFG", "Taula"))
        self.printAct.setText(_translate("TFG", "Imprimir"))

        self.actionCatal.setText(_translate("TFG", "Català"))
        self.actionCastellano.setText(_translate("TFG", "Español"))
        self.actionEnglish.setText(_translate("TFG", "English"))

        if self.histogram_is_done is not None:
            self.hist_lang()

        if self.table_is_done is not None:
            self.prop_lang()

        if self.graph_is_done is not None:
            self.scatter()

        if self.histogram_gauss_is_done is not None:
            self.hist_lang()



    def idioma_castellano(self, TFG):

        _translate = QtCore.QCoreApplication.translate
        self.actionCatal.setChecked(False)
        self.actionCastellano.setChecked(True)
        self.actionEnglish.setChecked(False)
        self.menuPropietats.setToolTip('Sobre la última segmentación realitzada')
        self.conceptes_act.setText(_translate("TFG", "Conceptos"))
        self.about_aim_Act.setText(_translate("TFG", "Objetivo"))
        self.about_gmm_act.setText(_translate("TFG", "GMM"))
        self.about_contrast_act.setText(_translate("TFG", "Contraste"))
        self.about_table_act.setText(_translate("TFG", "Tabla de características"))
        self.about_habilitar_act.setText(_translate("TFG", "Pan / zoom"))
        self.about_save_act.setText(_translate("TFG", "Guardar imágenes"))
        self.MenuAbout.setTitle(_translate("TFG", "La aplicación"))
        self.clickbutt.setText(_translate("TFG", "Pan / (x , y)"))
        self.clickbutt_2.setText(_translate("TFG", "Pan / (x , y)"))
        self.label_8.setText(_translate("TFG", "Tabla de características"))
        self.label_2.setText(_translate("TFG", "Imagen Procesada"))
        self.label_1.setText(_translate("TFG", "Imagen Original"))
        self.label_5.setText(_translate("TFG", "Histograma"))


        self.guardar_tabla.setText(_translate("TFG", "Guardar datos"))
        
        self.menuFitxer.setTitle(_translate("TFG", "Fichero"))

        self.menuHistograma.setTitle(_translate("TFG", "Histograma"))
        self.menuProcessament.setTitle(_translate("TFG", "Contraste"))
        self.menuSegmentaci.setTitle(_translate("TFG", "Segmentación"))
        self.menuK_Means.setTitle(_translate("TFG", "K-Means"))
        self.actionk_manual.setText(_translate("TFG", "Manual"))
        self.menuGMM.setTitle(_translate("TFG", "GMM"))
        self.menuPropietats.setTitle(_translate("TFG", "Propiedades"))

        self.menuGr_fic.setTitle(_translate("TFG", "Gráfico"))
        self.menuAjuda.setTitle(_translate("TFG", "Ayuda"))
        self.menuIdioma.setTitle(_translate("TFG", "Idioma"))
        self.actionSeleccionar_imatge.setText(_translate("TFG", "Seleccionar imagen"))

        self.actionGuardar.setText(_translate("TFG", "Guardar imagen procesada"))

        self.actionScreenshot.setText(_translate("TFG", "Captura de pantalla"))
        self.actionHistograma.setText(_translate("TFG", "Histograma"))
        self.about_hist_gauss_act.setText(_translate("TFG", "Histograma con Gausianas"))
        self.actionHistograma_amb_Gaussianes.setText(_translate("TFG", "Histograma con Gausianas"))
        self.actionContrast_gamma.setText(_translate("TFG", "Gamma"))
        self.actioncontrast_log.setText(_translate("TFG", "Logarítmico"))
        self.action_rea_Intensitat.setText(_translate("TFG", "Área / Intensidad"))
        self.actionOtsu.setText(_translate("TFG", "Otsu"))
        self.actionWatershed.setText(_translate("TFG", "Watershed"))
        self.actionAutom_tic.setText(_translate("TFG", "Automático"))
        self.actionFelzenszwalb.setText(_translate("TFG", "Felzenszwalb"))
        self.actionQuikshift.setText(_translate("TFG", "Quikshift"))
        self.actionGrayscale.setText(_translate("TFG", "Grayscale"))
        self.actionRGB.setText(_translate("TFG", "RGB"))
        self.actionPropietats.setText(_translate("TFG", "Tabla"))
        self.printAct.setText(_translate("TFG", "Imprimir"))

        self.trashbutt.setToolTip('Eliminar contraste')

        if self.histogram_is_done is not None:
            self.hist_lang()

        if self.table_is_done is not None:
            self.prop_lang()

        if self.graph_is_done is not None:
            self.scatter()

        if self.histogram_gauss_is_done is not None:
            self.hist_lang()

    def idioma_english(self, TFG):

        _translate = QtCore.QCoreApplication.translate
        self.actionCatal.setChecked(False)
        self.actionCastellano.setChecked(False)
        self.actionEnglish.setChecked(True)
        self.menuPropietats.setToolTip('Of the last segmentation')
        self.conceptes_act.setText(_translate("TFG", "Concepts"))
        self.about_aim_Act.setText(_translate("TFG", "Aim"))
        self.about_gmm_act.setText(_translate("TFG", "GMM"))
        self.about_contrast_act.setText(_translate("TFG", "Contrast"))
        self.about_table_act.setText(_translate("TFG", "Features table"))
        self.about_habilitar_act.setText(_translate("TFG", "Pan / zoom"))
        self.about_save_act.setText(_translate("TFG", "Save images"))
        self.MenuAbout.setTitle(_translate("TFG", "the application"))
        self.label_8.setText(_translate("TFG", "Features table"))
        self.label_2.setText(_translate("TFG", "Processed image"))
        self.label_1.setText(_translate("TFG", "Original Image"))
        self.label_5.setText(_translate("TFG", "Histogram"))
        self.clickbutt.setText(_translate("TFG", "Pan / (x , y)"))
        self.clickbutt_2.setText(_translate("TFG", "Pan / (x , y)"))

       
        self.guardar_tabla.setText(_translate("TFG", "Save data"))
        
        self.menuFitxer.setTitle(_translate("TFG", "File"))

        self.menuHistograma.setTitle(_translate("TFG", "Histogram"))
        self.menuProcessament.setTitle(_translate("TFG", "Contrast"))
        self.menuSegmentaci.setTitle(_translate("TFG", "Segmentation"))
        self.menuK_Means.setTitle(_translate("TFG", "K-Means"))
        self.actionk_manual.setText(_translate("TFG", "Manual"))
        self.menuGMM.setTitle(_translate("TFG", "GMM"))
        self.menuPropietats.setTitle(_translate("TFG", "Features"))
        
        self.menuGr_fic.setTitle(_translate("TFG", "Graph"))
        self.menuAjuda.setTitle(_translate("TFG", "Help"))
        self.menuIdioma.setTitle(_translate("TFG", "Language"))
        self.actionSeleccionar_imatge.setText(_translate("TFG", "Select image"))

        self.actionGuardar.setText(_translate("TFG", "Save processed image"))

        self.actionScreenshot.setText(_translate("TFG", "Screenshot"))
        self.actionHistograma.setText(_translate("TFG", "Histogram"))
        self.about_hist_gauss_act.setText(_translate("TFG", "Histogram with Gaussians"))
        self.actionHistograma_amb_Gaussianes.setText(_translate("TFG", "Histogram with Gaussians"))
        self.actionContrast_gamma.setText(_translate("TFG", "Gamma"))
        self.actioncontrast_log.setText(_translate("TFG", "Logarithmic"))
        self.action_rea_Intensitat.setText(_translate("TFG", "Area / Intensity"))
        self.actionOtsu.setText(_translate("TFG", "Otsu"))
        self.actionWatershed.setText(_translate("TFG", "Watershed"))
        self.actionAutom_tic.setText(_translate("TFG", "Automatic"))
        self.actionFelzenszwalb.setText(_translate("TFG", "Felzenszwalb"))
        self.actionQuikshift.setText(_translate("TFG", "Quikshift"))
        self.actionGrayscale.setText(_translate("TFG", "Grayscale"))
        self.actionRGB.setText(_translate("TFG", "RGB"))
        self.actionPropietats.setText(_translate("TFG", "Table"))
        self.printAct.setText(_translate("TFG", "Print"))

        

        self.trashbutt.setToolTip('Remove contrast filter')

        if self.histogram_is_done is not None:
            self.hist_lang()

        if self.table_is_done is not None:
            self.prop_lang()

        if self.graph_is_done is not None:
            self.scatter()

        if self.histogram_gauss_is_done is not None:
            self.hist_lang()

import para_fotos


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TFG = QtWidgets.QMainWindow()
    ui = Ui_TFG()
    ui.setupUi(TFG)
    TFG.show()
    sys.exit(app.exec_())
print(ui.__dict__.keys())