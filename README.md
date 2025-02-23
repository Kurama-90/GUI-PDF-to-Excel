# PDF to Excel Converter (GUI)

This is a PyQt5-based GUI application that allows users to convert PDF files into Excel files. The application provides multiple options for extracting data from PDFs, including tables, text, and OCR (Optical Character Recognition).

---

## Features

1. **PDF Table to Excel**: Extracts tables from a PDF and saves them into an Excel file.
2. **PDF Table/Sheet Excel**: Extracts multiple tables from a PDF and saves each table into a separate sheet in an Excel file.
3. **PDF to Excel**: Extracts all text from a PDF and saves it into an Excel file.
4. **OCR**: Uses Optical Character Recognition to extract text from scanned PDFs and saves it into an Excel file.

---

## Requirements

- Python 3.x
- PyQt5
- pdfplumber
- pandas
- PyMuPDF (fitz)
- pdf2image
- easyocr
- opencv-python (cv2)
- numpy
- poppler (+Add to PATH)

---

## Installation

1. Install the required Python packages:

   ```bash
   pip install PyQt5 pdfplumber pandas pymupdf pdf2image easyocr opencv-python numpy
   ```
   
## Clone or Download the Repository

Run the application:

```bash
python main.py
```
# Usage

### Select a PDF File:
Click the "File" button to select a PDF file from your system.

### Choose an Option:
Select one of the available options:

- **PDF Table to Excel**: Extracts tables from the PDF.
- **PDF Table/Sheet Excel**: Extracts multiple tables and saves each in a separate sheet.
- **PDF to Excel**: Extracts all text from the PDF.
- **OCR**: Uses OCR to extract text from scanned PDFs.

### Save the Output:
Click the "Ok" button to choose the output location and save the Excel file.

## Code Structure

### PdfConverter Class
This class contains static methods for handling PDF conversion:

- `convert_pdf_table_to_excel(pdf_path, output_file)`: Extracts tables from a PDF and saves them into an Excel file.
- `extract_tables_from_pdf(pdf_path)`: Extracts multiple tables from a PDF.
- `export_tables_to_excel(tables, output_excel_path)`: Exports extracted tables to an Excel file.
- `convert_pdf_text_to_excel(pdf_path, output_file)`: Extracts all text from a PDF and saves it into an Excel file.
- `process_ocr(pdf_path, output_file)`: Uses OCR to extract text from scanned PDFs.
- `export_to_excel(detections, output_file)`: Exports OCR-detected text to an Excel file.

### Ui_MainWindow Class
This class defines the GUI for the application:

- `setupUi(MainWindow)`: Sets up the main window, buttons, and options.
- `retranslateUi(MainWindow)`: Sets the text for UI elements.
- `openFileDialog()`: Opens a file dialog to select a PDF file.
- `onOkButtonClicked()`: Handles the conversion process based on the selected option.

## Example
1. Launch the application.
2. Select a PDF file using the "File" button.
3. Choose an option (e.g., "PDF Table to Excel").
4. Click "Ok" and select the output location.
5. The application will generate an Excel file with the extracted data.

## Notes
- Ensure that the selected PDF file is not corrupted or password-protected.
- For OCR functionality, the PDF should contain scanned images of text.

## License
This project is open-source and available under the GPL v3 License.

## Author
Kurama-90
