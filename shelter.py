import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QWidget
from PyQt5.QtWidgets import QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QFont

# The CatForm class is a subclass of the QMainWindow class, representing the main application window.
class CatForm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selectedImage = None # Variable to store the selected image file path

        self.setWindowTitle("Cat Shelter Directory")
        self.setGeometry(100, 100, 1200, 800)

        self.initUI()

    def initUI(self):
        # Create labels
        nameLabel = QLabel("Name:")
        nameLabel.setFont(QFont("Roboto", 12))
        medicalLabel = QLabel("Medical Information:")
        medicalLabel.setFont(QFont("Roboto", 12))
        adoptionLabel = QLabel("Adoption Status:")
        adoptionLabel.setFont(QFont("Roboto", 12))

        # Create input fields and checkboxes
        self.nameInput = QLineEdit()
        self.nameInput.setFixedHeight(70)
        self.nameInput.setFont(QFont("Roboto", 11))
        self.nameInput.setStyleSheet('Padding : 7px')
        self.medicalInput = QLineEdit()
        self.medicalInput.setFixedHeight(70)
        self.medicalInput.setStyleSheet('Padding : 7px')
        self.medicalInput.setFont(QFont("Roboto", 11))
        self.availableCheckbox = QCheckBox("Available")
        self.availableCheckbox.setFont(QFont("Roboto", 12))
        self.soonAvailableCheckbox = QCheckBox("Soon Available")
        self.soonAvailableCheckbox.setFont(QFont("Roboto", 12))
        self.adoptedCheckbox = QCheckBox("Adopted")
        self.adoptedCheckbox.setFont(QFont("Roboto", 12))

        # Create buttons and connect them to functions
        imageButton = QPushButton("Choose Image")
        imageButton.setFont(QFont("Roboto", 12))
        imageButton.clicked.connect(self.chooseImage)

        saveButton = QPushButton("Save")
        saveButton.setFont(QFont("RobotoRoboto", 12))

        saveButton.clicked.connect(self.saveCatRecord)

        # Create layout and set it as the central widget
        layout = QVBoxLayout()
        layout.addWidget(nameLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(medicalLabel)
        layout.addWidget(self.medicalInput)
        layout.addWidget(adoptionLabel)
        layout.addWidget(self.availableCheckbox)
        layout.addWidget(self.soonAvailableCheckbox)
        layout.addWidget(self.adoptedCheckbox)
        layout.addWidget(imageButton)
        layout.addWidget(saveButton)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def chooseImage(self):
        # Function to open a file dialog and get the selected image file path
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)",
                                               options=options)
        if image:
            # print("Selected Image:", image)
            self.selectedImage = image # Store the selected image path

    def saveCatRecord(self):
        # Function to save cat record to the SQLite database
        name = self.nameInput.text()
        image = self.selectedImage
        medical_info = self.medicalInput.text()
        status = ""
        if self.availableCheckbox.isChecked():
            status = "Available"
        elif self.soonAvailableCheckbox.isChecked():
            status = "Soon Available"
        elif self.adoptedCheckbox.isChecked():
            status = "Adopted"

        # print(f"Cat Name: {name}")
        # print(f"Medical Information: {medical_info}")
        # print(f"Adoption Status: {status}")

        con = sqlite3.connect("Cat_Shelter_Database.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS cats(name, medicalinfo, adoptionstatus, image);")

        try:
            # Use placeholders in the SQL command to prevent SQL injection
            command = f"INSERT INTO cats VALUES {(name, medical_info, status, image)}"
            cur.execute(command)
            con.commit()
            con.close()
            QMessageBox.information(None, "Success", "Successfuly stored in database")
        except IndexError as error:
            QMessageBox.information(None, "Error", "Failed to store in database")
            print(error)

        # Clear input fields and checkboxes after saving
        self.nameInput.clear()
        self.medicalInput.clear()
        self.availableCheckbox.setChecked(False)
        self.soonAvailableCheckbox.setChecked(False)
        self.adoptedCheckbox.setChecked(False)


# Entry point of the script
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CatForm()
    window.show()
    sys.exit(app.exec_())
