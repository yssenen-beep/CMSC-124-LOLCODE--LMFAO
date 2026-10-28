from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QLabel, QHeaderView
)
from PyQt6.QtCore import Qt

from interpreter.tokens import Token, TokenType
from interpreter.lex_analyzer import lex_le_analyzer # import lex analyzer
from interpreter.parser import Parser
import json

class ourGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOLCODE Lexical Analyzer for now")
        self.resize(900, 600)
        self.setMinimumSize(800, 500)
        self.init_ui()

    def init_ui(self):
        mainLO = QVBoxLayout() # top(code) to bottom(terminal)
        topLO = QHBoxLayout() # left(leftLO) to right(lexeme, symbol table)
        leftLO = QVBoxLayout() # top(file stuff) to bottom(code stuff)
        rightLO = QHBoxLayout() # left(lexeme) to right(symbol table)
        fileLO = QHBoxLayout() # left(file name) to right(open file btn)
        
        self.fileName = QLabel("No file selected") # shows the file currently open
        self.fileName.setMinimumWidth(100)

        self.fileBtn = QPushButton("Open File") # file opener
        self.fileBtn.clicked.connect(self.open_le_file) # connect to open le file func
        
        fileLO.addWidget(self.fileName, 1) # add ts
        fileLO.addWidget(self.fileBtn, 0)

        self.textEdit = QPlainTextEdit() # text editor
        self.textEdit.setPlaceholderText("Type something...")    
        self.textEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.textEdit.setMinimumWidth(250)

        leftLO.addLayout(fileLO) # add ts
        leftLO.addWidget(self.textEdit)

        self.lexemeT = QTableWidget(0, 2) # lexemes table
        self.lexemeT.setHorizontalHeaderLabels(["Lexeme", "Classification"])
        self.lexemeT.setMinimumWidth(200)
        self.lexemeT.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.symbolT = QTableWidget(0, 2) # symbol table
        self.symbolT.setHorizontalHeaderLabels(["Identifier", "Value"])
        self.symbolT.setMinimumWidth(200)
        self.symbolT.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        rightLO.addWidget(self.lexemeT) # add ts
        rightLO.addWidget(self.symbolT)

        topLO.addLayout(leftLO, 1) # Be of equal sizes
        topLO.addLayout(rightLO, 1)

        self.runBtn = QPushButton("RUN") # run button
        self.runBtn.clicked.connect(self.lexemeh_analysis)

        self.terminal = QPlainTextEdit() # output terminal
        self.terminal.setReadOnly(True) # can't type tho

        mainLO.addLayout(topLO) # add ts
        mainLO.addWidget(self.runBtn)
        mainLO.addWidget(self.terminal)

        self.setLayout(mainLO)

    def open_le_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open le File", "", "All vos Files (*)")    
        if file_path:
            self.fileName.setText(file_path)
            with open(file_path, "r", encoding="utf-8") as chosenFile:
                content = chosenFile.read()
                self.textEdit.setPlainText(content) # paste file

    def lexemeh_analysis(self):

        self.lexemeT.setRowCount(0) # reset lexeme table and terminal
        self.terminal.clear()

        content = self.textEdit.toPlainText() # get text from text editor
        tokens = lex_le_analyzer(content) # run ts on analyzer
        parser = Parser(tokens)
        test = parser.parse_program()
        print(json.dumps(test, indent=4))

        for token in tokens:
            if token.type == TokenType.LINEBREAK:
                continue
            row = self.lexemeT.rowCount() # check current row
            self.lexemeT.insertRow(row) # add new row
            self.lexemeT.setItem(row, 0, QTableWidgetItem(token.value)) # set columns
            self.lexemeT.setItem(row, 1, QTableWidgetItem(token.type.name))
