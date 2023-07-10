#Extract treatments information ("phases") from Save Spike Freqs1 file exported from Mobius
#Generates the "treatments.csv" File in the current directory
#Run with "python treatmentextract.py [Save Spikes filename]"
#Created EBM 9-17-2022
#Edited EBM 10-28-2022

import sys
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtWidgets import QPushButton, QLabel, QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, QTableView

#create global dataframe from the input file, clean up to draft treatments
pddata = pd.read_csv(open(sys.argv[1]), skiprows = 2, header = 0, usecols = [0,1,2])
dataextract = pddata[~pddata['phase'].isnull()]
dataextract = dataextract[~dataextract['time_secs'].isnull()]
lastrow = pd.DataFrame({'time_secs':[pddata['time_secs'].max()], 'phase':['END']})
dataextract = pd.concat([dataextract, lastrow], ignore_index = True)
dataextract['time_secs'] = dataextract['time_secs'].astype(int)

#enable interactive table, update the dataframe when cell values are changed
class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            print(self._data)
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)

class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.label = QLabel('Rows with empty Phase values will be removed')
        self.table = QTableView()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.model = PandasModel(dataextract)
        self.table.setModel(self.model)

        self.savebutton = QPushButton("Save / Close")
        self.layout.addWidget(self.savebutton)
        self.savebutton.clicked.connect(self.saveandclose)
#the button saves the 'treatments.csv' file, quits the program
    def saveandclose(self):
        savedata = dataextract[dataextract['phase'].str.len() > 0]
        savedata.to_csv('treatments.tsv', columns = ['time_secs', 'phase'], header = ['begin', 'label'], index=False, sep="\t")
        sys.exit()

w = 350
h = 600
app = QApplication(sys.argv)
window = MainWindow()
window.resize(w, h)
window.show()
app.exec_()