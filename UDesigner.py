import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QTextEdit, QCheckBox


def create_ustruct(name, fields, types):
    struct_def = f"USTRUCT(BlueprintType)\nstruct {name}\n{{\n\tGENERATED_BODY()\n\n"
    for field, field_type in zip(fields, types):
        struct_def += f"\tUPROPERTY(BlueprintReadWrite, EditAnywhere)\n\t{field_type} {field};\n"
    struct_def += "};\n"
    return struct_def


def create_uenum(name, enumerators):
    enum_def = f"UENUM(BlueprintType)\nenum class {name} : uint8\n{{\n"
    for enumerator in enumerators:
        enum_def += f"\t{enumerator} UMETA(DisplayName = \"{enumerator}\"),\n"
    enum_def += "};\n"
    return enum_def


def create_ufunction(name, return_type, params):
    function_def = f"UFUNCTION(BlueprintCallable, Category = \"{name}\")\n{return_type} {name}("
    function_def += ', '.join(params)
    function_def += ");\n"
    return function_def


class CreateUstructGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UDESIGNER")
        layout = QGridLayout()

        self.name_label = QLabel("Name>")
        self.name_entry = QLineEdit()
        self.fields_label = QLabel("Property Titles (separate w/commas)>")
        self.fields_entry = QLineEdit()
        self.field_types_label = QLabel("Property Types (separate w/commas)>")
        self.field_types_entry = QLineEdit()
        self.create_button = QPushButton(
            "Create", clicked=self.create_button_clicked)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.uenum_checkbox = QCheckBox("UENUM?")
        self.ufunction_checkbox = QCheckBox("UFUNCTION?")
        self.ustruct_checkbox = QCheckBox("USTRUCT?")

        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_entry, 0, 1)
        layout.addWidget(self.fields_label, 1, 0)
        layout.addWidget(self.fields_entry, 1, 1)
        layout.addWidget(self.field_types_label, 2, 0)
        layout.addWidget(self.field_types_entry, 2, 1)
        layout.addWidget(self.uenum_checkbox, 3, 0)
        layout.addWidget(self.ufunction_checkbox, 3, 1)
        layout.addWidget(self.ustruct_checkbox, 3, 2)
        layout.addWidget(self.create_button, 4, 0, 1, 3)
        layout.addWidget(self.output_text, 5, 0, 1, 3)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet(
            "background-color: #282828; color: Gray; QLineEdit { border: 1px solid black; }")
        self.setWindowIcon(QIcon('unrealMiniLogo.png'))

    def create_button_clicked(self):
        name = self.name_entry.text()
        fields = self.fields_entry.text().split(',')
        field_types = self.field_types_entry.text().split(',')

        if self.uenum_checkbox.isChecked():
            enum_def = create_uenum(name, fields)
            self.output_text.setPlainText(enum_def)
        elif self.ufunction_checkbox.isChecked():
            return_type = field_types[0]
            params = list(zip(field_types[1:], fields))
            formatted_params = [f"{t} {f}" for t, f in params]
            function_def = create_ufunction(name, return_type, formatted_params)
            self.output_text.setPlainText(function_def)
        elif self.ustruct_checkbox.isChecked():
            struct_def = create_ustruct(name, fields, field_types)
            self.output_text.setPlainText(struct_def)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = CreateUstructGUI()
    mainWin.show()
    sys.exit(app.exec())
