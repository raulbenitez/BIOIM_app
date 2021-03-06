from skimage import io, exposure
from skimage.filters import threshold_otsu, sobel    
from skimage.segmentation import clear_border, watershed, felzenszwalb, slic, quickshift
from sklearn.cluster import KMeans, AgglomerativeClustering
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.transform import resize
from skimage.color import label2rgb, rgb2gray
import numpy as np
from sklearn import mixture
from skimage.morphology import disk
from skimage.filters import median, gaussian
import skimage as sk
import itertools
from scipy import linalg
import scipy.stats as stats
import math
import scipy as scipy
from scipy.spatial import distance
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QImage, qRgb
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QTableWidgetItem
import pyqtgraph as pg
from skimage.measure import regionprops
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt


class Segmentada:
    def __init__(self, process=None, label = None, imaori = None, histogram_is_done=None, table_is_done=None, graph_is_done=None, histogram_gauss_is_done=None):
        self.process = process
        self.label = label
        self.imaori = imaori
        self.histogram_is_done = histogram_is_done
        self.table_is_done = table_is_done
        self.graph_is_done = graph_is_done
        self.histogram_gauss_is_done = histogram_gauss_is_done

    def pre_segm(self,img_op):
        self.actionPropietats.setEnabled(True)
        if self.process is not None: #si ya se ha hecho una corrección que utilice esa imagen para empezar, no la original
            self.imaori = self.process
        else:
            self.imaori=rgb2gray(self.img_op)
    
    def toQImage(self, im):
        gray_color_table = [qRgb(0, i, 0) for i in range(256)]

        if im is None:
            return QImage()

        im_255 = im*255 #float64 define el rango de [0-255] de grayscale como [0-1] con decimales, hay que multiplicar por 255.
        img_8 = im_255.astype(np.uint8) #entonces la convertimos a int8

        if img_8.dtype == np.uint8:

            img_8 = np.require(img_8, np.uint8, 'C')

            if len(img_8.shape) == 2: #dependiendo del número de canales que tenga, significará que la imagen es en grayscale, RGB o ARGB
                self.qim = QImage(img_8.data, img_8.shape[1], img_8.shape[0], img_8.strides[0], QImage.Format_Indexed8)#transformamos a QImage
                self.qim.setColorTable(gray_color_table)


            elif len(img_8.shape) == 3: #si el shape de la I es 3, es porque tenemos (x_pix, y_pix, canales)
                if img_8.shape[2] == 3: #ahora podemos tener 3 canales (RGB)
                    self.qim = QImage(img_8.data, img_8.shape[1], img_8.shape[0], img_8.strides[0], QImage.Format_RGB888);


                elif img_8.shape[2] == 4: #o tener 4 canales (ARGB)
                    self.qim = QImage(img_8.data, img_8.shape[1], img_8.shape[0], img_8.strides[0], QImage.Format_ARGB32);


        self.imageLabel_2.setPhoto(QtGui.QPixmap(self.qim)) #qim es la imagen ya en qImage


    def delete_process(self):
        self.process = None
        msg = QMessageBox()
        if self.actionCatal.isChecked():
            msg.setText("Contrast eliminat! " "Torna a segmentar")
        if self.actionCastellano.isChecked():
            msg.setText("Contraste eliminado! " "Vuelve a segmentar")
        if self.actionEnglish.isChecked():
            msg.setText("Contrast removed! " "Repeat the segmentation")
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

##########################################

    def gammacorrection(self, img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.imaori=rgb2gray(self.img_op)#para la corrección gamma primero pasamos la imagen de rgb a escala de grises
        self.process = exposure.adjust_gamma(self.imaori, 2)#ajustamos la exposición según el ajuste gamma
        self.toQImage(self.process) #convertimos la imagen de formato float64 a QImage para poder visualizarla, mediante una función


    def logcorrection(self, img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.imaori=rgb2gray(self.img_op)
        self.process = exposure.adjust_log(self.imaori, 1)#hace lo mismo pero con ajuste logarítmico
        self.toQImage(self.process)


###########################################33


    def segm_otsu(self, img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        self.thresh = threshold_otsu(self.imaori)
        bw = closing(self.imaori < self.thresh, square(3))
        cleared = clear_border(bw)
        self.label = label(cleared)
        self.segmen = label2rgb(self.label, image=self.imaori)
        self.toQImage(self.segmen)


    def segm_water(self,img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        gradient = sobel(self.imaori)
        self.label = watershed(gradient, markers=600)
        self.segmen=label2rgb(self.label, self.imaori)
        self.toQImage(self.segmen)


    def segm_k(self,img_op): #detecta automàticament el número de clusters que vol escollir
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        self.label = slic(self.imaori, compactness=0.2, n_segments=600)
        self.segmen = label2rgb(self.label, self.imaori, kind='avg')
        self.toQImage(self.segmen)


    def segm_felz(self,img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        self.label = felzenszwalb(self.imaori, scale=100, sigma=0.5, min_size=50)
        self.segmen = label2rgb(self.label, self.imaori, kind='avg')
        self.toQImage(self.segmen)


    def segm_quick(self,img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        self.label = quickshift(self.imaori, kernel_size=5, ratio=1.0, max_dist=10, return_tree=False, sigma=0, convert2lab=False, random_seed=42)
        self.segmen = label2rgb(self.label, self.imaori, kind='avg')
        self.toQImage(self.segmen)

    def segm_k_manual(self,img_op, n_clusters):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        v_I = self.imaori.reshape(self.imaori.shape[0]*self.imaori.shape[1],1) 
        km = KMeans(n_clusters=self.n_clusters).fit(v_I)
        pred = km.predict(v_I)
        v_agg= np.logical_not(pred)
        imafin = np.array(v_agg).reshape(self.imaori.shape[0],self.imaori.shape[1]) # Shape back result as image
        self.label = label(imafin)
        self.segmen = label2rgb(self.label, self.imaori, kind='avg')
        self.toQImage(self.segmen)

    def manual(self, img_op):
        if self.actionCatal.isChecked() or self.actionCastellano.isChecked():
            self.n_clusters, result = QInputDialog.getInt(self,'Input','Número de clusters') #Diàlog on el usuari especifica el número de clusters

        if self.actionEnglish.isChecked():
            self.n_clusters, result = QInputDialog.getInt(self,'Input','Number of clusters')


        if result == True:
            if 1<self.n_clusters<51 or type(self.n_clusters) != int:
                self.segm_k_manual(self.img_op, self.n_clusters)
            else:
                ms = QMessageBox()
                if self.actionCatal.isChecked():
                    ms.setText("El número de clusters ha de ser un enter al rang [2,50]")
                if self.actionCastellano.isChecked():
                    ms.setText("El número de clusters debe ser un entero en el rango [2,50]")
                if self.actionEnglish.isChecked():
                    ms.setText("The number of clusters must be an integrer in range [2,50]")
                
                ms.setWindowTitle("Error")
                ms.setIcon(QMessageBox.Critical)
                y = ms.exec_()


    def segmentacio_gauss_g(self,img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(True)
        self.pre_segm(self.img_op)
        imaorif = median(self.imaori, disk(1))
        self.imaori = median(imaorif, disk(2))
        v_I_train = np.reshape(self.imaori,(self.imaori.shape[0]*self.imaori.shape[1],1)) #convertir a vector
        #self.v_I_train = v_I_train
        #calcula el BIC per trobar el número de gaussianes òptim
        NMAX = 10
        bic = []
        for kG in np.arange(1,NMAX+1):
            gmm = mixture.GaussianMixture(n_components=kG).fit(v_I_train)
            bic.append(gmm.bic(v_I_train)) #cada cop va afegint el bic amb kG+1, així ho tens tot en un vector i pots calcualr el mínim

        idx_winner = np.argmin(bic)
        gmmw = mixture.GaussianMixture(n_components=idx_winner).fit(v_I_train)
        means0= gmmw.means_.reshape(1,-1)
        means = np.array(means0).ravel()

        M = np.zeros([len(means),2])
        for x in range (0,len(means)):
            M[x][0] = means[x]
            M[x][1] = gmmw.weights_[x]
         
        sortedm = M[M[:,0].argsort()]
        means_def = []
        x = 0
        while x <=len(means)-2:
            if sortedm[x,0]+10<sortedm[x+1,0]:
                means_def.append(sortedm[x,0]) #en cas de que no estiguin aprop, l'afegim directament
                x = x+1
                if x==len(means)-1:
                    means_def.append(sortedm[x,0]) #si el penúltim average i el últim no estan a prop, com que per l'últim ja no podem
                    #seguir comparant amb cap altre següent, simplement l'afegim. De fet no fa falta comparar ja que ja ha sigut comparat
            else: #si estan a prop hem de mirar quin té un pes més alt, i aquest serà el que es quedi.
                if sortedm[x,1]>sortedm[x+1,1]:
                    means_def.append(sortedm[x,0])
                    x = x+2 #saltem dues posicions perquè la següent ja sabem que no és rellevant, està a prop d'aquesta i té un pes inferior.
                    if x == len(means)-1:
                        means_def.append(sortedm[x,0])
                else:
                    means_def.append(sortedm[x+1,0])
                    x = x+1
                    
        means_def = np.unique(means_def)
        means_def = np.reshape(means_def,[len(means_def),1])
        self.gmw2 = mixture.GaussianMixture(n_components=len(means_def), means_init=means_def).fit(v_I_train)
        v_agg = self.gmw2.fit_predict(v_I_train)
        imafin = np.array(v_agg).reshape(self.imaori.shape[0],self.imaori.shape[1])# Shape back result as image
        self.label = label(imafin)
        self.segmen = label2rgb(imafin, self.imaori, kind='avg')
        self.toQImage(self.segmen)


    def segmentacio_gauss_color(self,img_op):
        self.actionHistograma_amb_Gaussianes.setEnabled(False)
        self.pre_segm(self.img_op)
        R = self.imaori[:,:,0]
        G = self.imaori[:,:,1]
        B = self.imaori[:,:,2]
        v_R = np.reshape(R,(R.shape[0]*R.shape[1],1))
        v_G = np.reshape(G,(G.shape[0]*G.shape[1],1))
        v_B = np.reshape(B,(B.shape[0]*B.shape[1],1))
        MT = np.zeros([len(v_R),3])
        for x in range (0,len(v_R)):
            MT[x,0] = v_R[x]
            MT[x,1] = v_G[x]
            MT[x,2] = v_B[x]
        v_I_train = MT
        lowest_bic = np.infty
        bic = []
        n_components_range = range(1, 11)
        cv_types = ['spherical', 'tied', 'diag', 'full']
        for cv_type in cv_types:
            for n_components in n_components_range:
                # Fit a Gaussian mixture with EM
                gmm = mixture.GaussianMixture(n_components=n_components,
                                              covariance_type=cv_type)
                gmm.fit(v_I_train)
                bic.append(gmm.bic(v_I_train))
                if bic[-1] < lowest_bic:
                    lowest_bic = bic[-1]
                    best_gmm = gmm

        bic = np.array(bic)
        gmmw = best_gmm # GUANYADOR
        bars = []
        M = np.zeros([np.size(gmmw.means_[:,0]),4])
        g = [[255,255,255]]
        p = [[0,0,0]]
        maxim = distance.cdist(g, p, 'euclidean')
        eucl = distance.cdist(gmmw.means_, gmmw.means_, 'euclidean')
        eucl_porc = eucl*100/maxim
        means = gmmw.means_
        todel = [] #gauss to delete
        for i in range (0,np.size(eucl_porc[0])):
            for j in range (0,np.size(eucl_porc[1])):
                if eucl_porc[i,j] <= 10 and eucl_porc[i,j]!=0:
                    if gmmw.weights_[i]>gmmw.weights_[j]:
                        todel.append(j)
                    else:
                        todel.append(i)
                        
        todel = np.unique(todel)
        means_def = []
        for y in range (0,10):
            if y not in todel:
                means_def.append(means[y,:])
        print(means_def)
        gmw2 = mixture.GaussianMixture(n_components=len(means_def), means_init=means_def, covariance_type=gmmw.covariance_type).fit(v_I_train)
        v_agg2 = gmw2.predict(MT) #recorda que v_I_train es la matriu MT
        imafin = np.array(v_agg2).reshape(imaori.shape[0],imaori.shape[1])
        self.label = label(imafin)
        self.segmen = label2rgb(imafin, self.imaori, kind='avg')
        self.toQImage(self.segmen)

###########################################3333

    def histograma(self, img_op):
        self.pre_segm(self.img_op)
        v_I_train = (np.reshape(self.imaori,(self.imaori.shape[0]*self.imaori.shape[1],1)))*255 #convertir a vector
        y,x = np.histogram(v_I_train, bins=256)
        pen = pg.mkBrush('c')
        self.histogram_is_done = 1

        y = y*100/np.sum(y)

        self.hist_lang()

        self.histogram.plot(x, y, stepMode=True, fillLevel=0, brush=pen)

    def hist_lang(self):
        if self.actionCatal.isChecked():
            self.histogram.setLabel('left', 'Percentatge de píxels (%)', color='white', size=50)
            self.histogram.setLabel('bottom', 'Nivell de píxel [0-255]')

        elif self.actionCastellano.isChecked():
            self.histogram.setLabel('left', 'Porcentaje de píxeles (%)', color='white', size=50)
            self.histogram.setLabel('bottom', 'Nivel de píxel [0-255]')

        elif self.actionEnglish.isChecked():
            self.histogram.setLabel('left', 'Pixel percentage (%)', color='white', size=50)
            self.histogram.setLabel('bottom', 'Pixel level [0-255]')

    def hist_gauss(self):
        cov = np.reshape(self.gmw2.covariances_, len(self.gmw2.covariances_),1)
        #print(cov)
        means = np.reshape(self.gmw2.means_, len(self.gmw2.means_),1)
        #print(means)
        self.pre_segm(self.img_op)
        v_I_train = (np.reshape(self.imaori,(self.imaori.shape[0]*self.imaori.shape[1],1)))*255 #convertir a vector
        y,x = np.histogram(v_I_train, bins=256)
        
        self.histogram_gauss_is_done = 1

        y = y*100/np.sum(y)

        self.hist_lang()
        brush = pg.mkBrush('c')
        self.histogram.plot(x, y, stepMode=True, fillLevel=0, brush=brush)
        self.histogram.addLegend(size = (100,20), offset=(-10,5))


        c = [(0,0,0),(255,255,0),(255,0,0),(192,192,192),(255,0,128),(255,128,0),(128,0,128),(0,255,0),(0,0,255),(166,83,0)]
        for h in range (0,len(cov)):
            mu = means[h]
            variance = cov[h]
            sigma = math.sqrt(variance)
            x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
            u = (scipy.stats.norm.pdf(x, mu, sigma)/scipy.stats.norm.pdf(mu, mu, sigma))*max(y)*self.gmw2.weights_[h]*0.7

            pen = pg.mkPen(color=c[h], width=3)
            
            self.histogram.plot(x, u, pen=pen, name=("\u03BC :" + str(round(mu,1)) + " ,\u03C3: " + str(round(cov[h],1))))

        

#####################################################

    def prop(self): #propiedades de la segmentada (que era la Otsu)
        self.table_is_done = 1
        self.regions=regionprops(self.label, intensity_image=self.imaori) #en regions guarda las propiedades encontradas por la función regionprops
        
        self.areas = [prop.area for prop in self.regions] #después va diciendo para cada propiedad a cuál corresponde de las que se han guardado en regions.
        self.centroids=[prop.centroid for prop in self.regions] #lo hace para la característica; etiqueta (qué etiqueta se le ha dado a un área al segmentarla), área, intensidad y centroide.
        self.labels= [prop.label for prop in self.regions]
        self.inte= [prop.mean_intensity for prop in self.regions]
        
        self.taula.setRowCount(len(self.labels)+1)
        self.taula.setColumnCount(4)
        label_str = []
        areas_str = []
        centroids_str = []
        inte_str = []
        for x in range(0,len(self.labels)):
            label_str.append(str(self.labels[x]))
            areas_str.append(str(self.areas[x]))
            centroids_str.append(str(self.centroids[x]))
            inte_str.append(str(self.inte[x]*100))



        self.taula.setItem(0,0, QTableWidgetItem(""))
        self.taula.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.taula.item(0, 0).setBackground(QtGui.QColor(0,183,0))

        
        
        self.taula.setItem(0,2, QTableWidgetItem("(x , y)"))
        self.taula.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.taula.item(0, 2).setBackground(QtGui.QColor(0,183,0))

        self.taula.setItem(0,3, QTableWidgetItem("e-100"))
        self.taula.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.taula.item(0, 3).setBackground(QtGui.QColor(0,183,0))

        self.taula.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.guardar_tabla.setEnabled(True)
        self.action_rea_Intensitat.setEnabled(True)

        for row in range(1,len(label_str)+1):
            self.taula.setItem(row,0, QTableWidgetItem(label_str[row-1]))
            self.taula.item(row, 0).setBackground(QtGui.QColor(237,237,239))
            self.taula.item(row, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.taula.setItem(row,1, QTableWidgetItem(areas_str[row-1]))
            self.taula.item(row, 1).setBackground(QtGui.QColor(237,237,239))
            self.taula.item(row, 1).setTextAlignment(QtCore.Qt.AlignCenter)

            self.taula.setItem(row,2, QTableWidgetItem(centroids_str[row-1]))
            self.taula.item(row, 2).setBackground(QtGui.QColor(237,237,239))
            self.taula.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)

            self.taula.setItem(row,3, QTableWidgetItem(inte_str[row-1]))
            self.taula.item(row, 3).setBackground(QtGui.QColor(237,237,239))
            self.taula.item(row, 3).setTextAlignment(QtCore.Qt.AlignCenter)

        self.prop_lang()

    def prop_lang(self):
        if self.actionCatal.isChecked():
            self.taula.setHorizontalHeaderLabels(('Etiqueta','Àrea','Centroide','Intensitat'))
            self.taula.setItem(0,1, QTableWidgetItem("Núm. píxels"))

        elif self.actionCastellano.isChecked():
            self.taula.setHorizontalHeaderLabels(('Etiqueta','Área','Centroide','Intensidad'))
            self.taula.setItem(0,1, QTableWidgetItem("Núm. píxeles"))

        elif self.actionEnglish.isChecked():
            self.taula.setHorizontalHeaderLabels(('Label','Area','Centroid','Intensity'))
            self.taula.setItem(0,1, QTableWidgetItem("Num. pixels"))
        
        self.taula.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.taula.item(0, 1).setBackground(QtGui.QColor(0,183,0))

    def scatter(self):
        self.graph_is_done = 1
        rng = np.random.RandomState(0)

        colors = rng.rand(len(self.areas))

        # plot the data
        self.fig = plt.figure()
        
        self.ax = self.fig.add_subplot(1, 1, 1)
        
        if self.actionCatal.isChecked():
            self.ax.clear()
            self.fig.canvas.set_window_title('Gràfic')
            self.ax.set_title('Àrea / Intensitat', fontsize=20)
            self.ax.set_xlabel('Intensitat', fontsize=15)
            self.ax.set_ylabel('Àrea', fontsize=18)

        elif self.actionCastellano.isChecked():
            self.ax.clear()
            self.fig.canvas.set_window_title('Gráfico')
            self.ax.set_title('Área / Intensidad', fontsize=20)
            self.ax.set_xlabel('Intensidad', fontsize=15)
            self.ax.set_ylabel('Área', fontsize=18)

        elif self.actionEnglish.isChecked():
            self.ax.clear()
            self.fig.canvas.set_window_title('Graph')
            self.ax.set_title('Area / Intensity', fontsize=20)
            self.ax.set_xlabel('Intensity', fontsize=15)
            self.ax.set_ylabel('Area', fontsize=18)

        self.ax.scatter(self.inte, self.areas, c=colors, alpha=0.3,
                    cmap='magma')
        
        self.fig.patch.set_facecolor(color= '#ededef')
                
        plt.show()


    def handleSave(self):

        self.list = {'Etiqueta': self.labels,'Area':self.areas,'Centroide': self.centroids, 'Intensitat':self.inte}
        self.data = pd.DataFrame(self.list, columns=['Etiqueta','Area','Centroide','Intensitat'])

        path, ok = QFileDialog.getSaveFileName(
                self, 'Guardar Fitxer', '', 'CSV(*.csv)')

        if ok:
            self.data.to_csv(path, index = None, header=True)
