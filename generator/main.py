from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from generator_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.start_home_position = """(Move to work position)
$H
G90 G20
G0 X0 Y0
G0 Z0 \n
"""

        self.end_home_position = """(Move back to work position)
G0 Z0.85
G0 X0 Y0
"""
        self.xoffset = ""
        self.yoffset = ""
        self.xyspeed = ""
        self.zspeed = ""
        self.xyextracut = ""
        self.cutdepth = ""
        self.inputlength = ""
        self.inputwidth = ""
        self.inputthickness = ""
        self.outputlength = ""
        self.outputwidth = ""

        self.val_xoffset = 0.0
        self.val_yoffset = 0.0
        self.val_xyspeed = 0.0
        self.val_zspeed = 0.0
        self.val_xyextracut = 0.0
        self.val_cutdepth = 0.0
        self.val_inputlength = 0.0
        self.val_inputwidth = 0.0
        self.val_inputthickness = 0.0
        self.val_outputlength = 0.0
        self.val_outputwidth = 0.0

        self.data_x = []
        self.data_y = []
        self.no_rows = 0
        self.no_columns = 0

        self.actions()
        self.show()

    def actions(self):
        self.pushButton_generate.clicked.connect(self.operator_save)
        self.pushButton_generate.setCheckable(True)
        self.pushButton_generate.toggle()

    def operator_save(self):
        self.xoffset = self.lineEdit_xoffset.text()
        self.yoffset = self.lineEdit_yoffset.text()
        self.xyspeed = self.lineEdit_xyspeed.text()
        self.zspeed = self.lineEdit_zspeed.text()
        self.xyextracut = self.lineEdit_xyextracut.text()
        self.cutdepth = self.lineEdit_cutdepth.text()
        self.inputlength = self.lineEdit_inputlength.text()
        self.inputwidth = self.lineEdit_inputwidth.text()
        self.inputthickness = self.lineEdit_thickness.text()
        self.outputlength = self.lineEdit_outputlength.text()
        self.outputwidth = self.lineEdit_outputwidth.text()

        if(self.xoffset == "" or self.yoffset == "" or self.xyspeed == "" or self.zspeed == ""
           or self.xyextracut == "" or self.cutdepth == "" or self.inputlength == "" or self.inputwidth == ""
           or self.inputthickness == "" or self.outputlength == "" or  self.outputwidth == ""):
            self.show_popup_nullvalue()

        self.val_xoffset = float(self.xoffset)
        self.val_yoffset = float(self.yoffset)
        self.val_xyspeed = float(self.xyspeed)
        self.val_zspeed = float(self.zspeed)
        self.val_xyextracut = float(self.xyextracut)
        self.val_cutdepth = float(self.cutdepth)
        self.val_inputlength = float(self.inputlength)
        self.val_inputwidth = float(self.inputwidth)
        self.val_inputthickness = float(self.inputthickness)
        self.val_outputlength = float(self.outputlength)
        self.val_outputwidth = float(self.outputwidth)

        if(self.val_inputlength < 12 or self.val_inputlength > 96 or self.val_inputwidth < 12 or self.val_inputwidth > 48
           or self.val_outputlength < 1 or self.val_outputlength > 96 or self.val_outputwidth < 1 or self.val_outputwidth > 48):
            self.show_popup_overvalue()

        self.find_rows_columns()
        self.create_file()

    def find_rows_columns(self):
        self.no_rows = int((self.val_inputlength - 0.1)/self.val_outputlength)
        self.no_columns = int((self.val_inputwidth - 0.1)/self.val_outputwidth)
        # print("created no of rows and columns")

    def show_popup_nullvalue(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error while generating Gcode")
        msg.setText("Fill all the Text box")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)

        msg.buttonClicked.connect(self.popup_button_nullvalue)
        x = msg.exec_()

    def popup_button_nullvalue(self, i):
        if (i.text() == "Cancel"):
            exit()
        if (i.text() == "Retry"):
            exit()

    def show_popup_overvalue(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error while generating Gcode")
        msg.setText("Over value, Please Enter the correct value")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)

        msg.buttonClicked.connect(self.popup_button_overvalue)
        x = msg.exec_()

    def popup_button_overvalue(self, i):
        if (i.text() == "Cancel"):
            exit()
        if (i.text() == "Retry"):
            exit()

    # Function to convert
    def listToString(self, s):
        # initialize an empty string
        str1 = ""
        # return string
        return (str1.join(s))

    # Function to generate along x axis movement Gcode
    def x_rows(self, no_rows):
        self.data_x.append("(start of the rows along x axis movement)\n")
        for x in range(self.no_rows):
            self.new_row_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 X{} F{}
G01 Z{} F{}\n\n""".format(self.val_xoffset, (self.val_outputlength * (x+1)), self.val_xyspeed,
                               self.val_cutdepth, self.val_zspeed,
                               self.val_inputwidth + self.val_xyextracut, self.val_xyspeed,
                               self.val_cutdepth, self.val_zspeed)
            self.data_x.append(self.new_row_string)

        return self.listToString(self.data_x)

    # Function to generate along y axis movement Gcode
    def y_columns(self, no_columns):
        self.data_y.append("(start of the column along y axis movement)\n")
        for y in range(self.no_columns):
            new_column_string = """G01 X{} Y{} F{}
G01 Z-{} F{}
G01 y{} F{}
G01 Z{} F{}\n\n""".format((self.val_outputwidth) * (y+1), self.val_yoffset, self.val_xyspeed,
                               self.val_cutdepth, self.val_zspeed,
                               self.val_inputlength + self.val_xyextracut, self.val_xyspeed,
                               self.val_cutdepth, self.val_zspeed)
            self.data_y.append(new_column_string)

        return self.listToString(self.data_y)

    def create_file(self):
        f = open("Gcode.nc", "w")
        f.write(self.start_home_position)             # start of the G code -- work position zero Gcode
        f.write(self.x_rows(self.no_rows))            # start of the rows (along x movement)
        f.write(self.y_columns(self.no_columns))          # start of the columns (along y movement)
        f.write(self.end_home_position)             # End of Gode -- return to home
        f.close()

        self.label_finshed.setText("Generated")
        self.label_finshed.setStyleSheet("background-color: lightgreen")
        print("End of the code")

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Gcode Generator")

    window = MainWindow()
    app.exec_()
