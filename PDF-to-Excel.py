from PyQt5.QtCore import QCoreApplication, QMetaObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QRadioButton, QPushButton, QPlainTextEdit, QStatusBar, QWidget, QFileDialog, QMessageBox
import os

class PdfConverter:
    @staticmethod
    def convert_pdf_table_to_excel(pdf_path, output_file):
        import pdfplumber
        import pandas as pd
        
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_tables.extend(table)
        if not all_tables:
            print("Aucune table trouvée dans le PDF.")
            return None
        df = pd.DataFrame(all_tables[1:], columns=all_tables[0])
        df.to_excel(output_file, index=False)
        print(f"Le fichier Excel a été généré avec succès : {output_file}")
        return output_file

    @staticmethod
    def extract_tables_from_pdf(pdf_path):
        import fitz  # PyMuPDF
        
        pdf_document = fitz.open(pdf_path)
        tables = []
        for page_num in range(len(pdf_document)):
            print(f"Traitement de la page {page_num + 1}...")
            page = pdf_document[page_num]
            tables_in_page = page.find_tables()
            for table in tables_in_page:
                table_data = table.extract()
                tables.append(table_data)
        pdf_document.close()
        return tables

    @staticmethod
    def export_tables_to_excel(tables, output_excel_path):
        import pandas as pd
        
        with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
            for i, table in enumerate(tables):
                df = pd.DataFrame(table[1:], columns=table[0])
                df.to_excel(writer, sheet_name=f"Table_{i + 1}", index=False)
        print(f"Fichier Excel généré : {output_excel_path}")

    @staticmethod
    def convert_pdf_text_to_excel(pdf_path, output_file):
        import fitz  # PyMuPDF
        import pandas as pd
        
        doc = fitz.open(pdf_path)
        extracted_text = [page.get_text("text") for page in doc]
        doc.close()
        df = pd.DataFrame({"Texte extrait": extracted_text})
        df.to_excel(output_file, index=False)
        print(f"Le fichier Excel a été généré avec succès : {output_file}")
        return output_file

    @staticmethod
    def process_ocr(pdf_path, output_file):
        from pdf2image import convert_from_path
        import easyocr
        import cv2
        import numpy as np
        
        images = convert_from_path(pdf_path)
        print(f"{len(images)} pages converties en images.")
        detections = []
        reader = easyocr.Reader(['fr'])
        for i, image in enumerate(images):
            print(f"Extraction du texte de la page {i + 1}...")
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            result = reader.readtext(image_cv)
            detections.append(result)
        PdfConverter.export_to_excel(detections, output_file)
        print(f"Le fichier Excel a été généré avec succès : {output_file}")
        return output_file

    @staticmethod
    def export_to_excel(detections, output_file):
        import pandas as pd
        
        data = {}
        for page_num, page_detections in enumerate(detections):
            for (bbox, text, prob) in page_detections:
                x0, y0 = bbox[0]
                x1, y1 = bbox[2]
                row = int(y0 // 20)
                col = int(x0 // 20)
                if (row, col) not in data:
                    data[(row, col)] = text
                else:
                    data[(row, col)] += " " + text
        df = pd.DataFrame.from_dict(data, orient="index", columns=["Text"])
        df.index = pd.MultiIndex.from_tuples(df.index, names=["Row", "Column"])
        df = df.unstack().fillna("")
        df.to_excel(output_file)
        print(f"Fichier Excel généré : {output_file}")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.setMinimumSize(750, 227)
        MainWindow.setMaximumSize(750, 227)
        MainWindow.setAnimated(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Option = QGroupBox(self.centralwidget)
        self.Option.setObjectName("Option")
        self.Option.setEnabled(True)
        self.Option.setGeometry(560, 20, 171, 181)

        self.radioButton = QRadioButton(self.Option)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setGeometry(10, 30, 141, 20)
        self.radioButton.setChecked(True)

        self.radioButton_2 = QRadioButton(self.Option)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setGeometry(10, 70, 181, 16)

        self.radioButton_3 = QRadioButton(self.Option)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setGeometry(10, 110, 95, 20)

        self.radioButton_4 = QRadioButton(self.Option)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.setGeometry(10, 150, 95, 20)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(450, 30, 93, 31)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setGeometry(190, 120, 93, 31)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setGeometry(20, 30, 421, 31)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.openFileDialog)
        self.pushButton_2.clicked.connect(self.onOkButtonClicked)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "PDF to EXCEL (Kurama-90)", None))
        self.Option.setTitle(QCoreApplication.translate("MainWindow", "Option", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", "PDF table to Excel", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", "PDF table/Sheet Excel", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", "PDF to Excel", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", "OCR", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "File", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "Ok", None))

    def openFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(None, "Select PDF File", "", "PDF Files (*.pdf)", options=options)
        if filePath:
            self.plainTextEdit.setPlainText(filePath)

    def onOkButtonClicked(self):
        pdf_path = self.plainTextEdit.toPlainText().strip()
        if not os.path.exists(pdf_path):
            QMessageBox.warning(None, "Erreur", "Le fichier PDF n'existe pas.")
            return

        output_file, _ = QFileDialog.getSaveFileName(None, "sauvegarder", "", "Excel Files (*.xlsx)", options=QFileDialog.Options())
        if not output_file:
            QMessageBox.warning(None, "Erreur", "Aucun fichier de sortie sélectionné.")
            return
        if not output_file.lower().endswith(".xlsx"):
            output_file += ".xlsx"

        if self.radioButton.isChecked():
            output_path = PdfConverter.convert_pdf_table_to_excel(pdf_path, output_file)
        elif self.radioButton_2.isChecked():
            tables = PdfConverter.extract_tables_from_pdf(pdf_path)
            PdfConverter.export_tables_to_excel(tables, output_file)
            output_path = output_file
        elif self.radioButton_3.isChecked():
            output_path = PdfConverter.convert_pdf_text_to_excel(pdf_path, output_file)
        elif self.radioButton_4.isChecked():
            output_path = PdfConverter.process_ocr(pdf_path, output_file)

        if output_path:
            QMessageBox.information(None, "Succès", f"Le fichier Excel a été généré : {output_path}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())