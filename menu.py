from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QBrush, QPainter
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QStackedWidget, QWidget, QLabel, QHBoxLayout, QPushButton, \
    QScrollArea, QTextBrowser
from custom_button import CustomButton as button
from go import Go

class Menu(QDialog):
    def __init__(self):
        super().__init__()
        self.go_window = None
        self.stacked_widget = None
        self.current_page_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menu')
        self.setGeometry(200, 200, 800, 600)

        # QDialog Layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Espace extensible à gauche
        passbtn = button('Pass', 'rgb(221,221,221)')
        passbtn.setFixedSize(100,25)
        top_layout.addWidget(passbtn)
        main_layout.addLayout(top_layout)

        passbtn.clicked.connect(self.launchGame)

        # Create a Satcked to have all the page at the same place
        self.stacked_widget = QStackedWidget(self)

        # Créer les pages et les ajouter au widget empilable
        self.pages = []
        for i in range(5):
            page = QWidget(self)
            self.addText(page, i)
            self.pages.append(page)
            self.stacked_widget.addWidget(page)

        # Ajouter le widget empilable au layout principal
        main_layout.addWidget(self.stacked_widget)

        # Ajouter des boutons de navigation (Next et Previous)
        nav_layout = QHBoxLayout()
        main_layout.addLayout(nav_layout)

        btn_previous = button('Previous', 'rgb(221,221,221)')
        btn_previous.clicked.connect(self.show_previous_page)
        nav_layout.addWidget(btn_previous)

        btn_next = button('Next', "rgb(221,221,221)")
        btn_next.clicked.connect(self.show_next_page)
        nav_layout.addWidget(btn_next)

        # Afficher la première page par défaut
        self.current_page_index = 0
        self.stacked_widget.setCurrentIndex(self.current_page_index)
        self.show()

    def show_previous_page(self):
        # Afficher la page précédente
        self.current_page_index -= 1
        if self.current_page_index < 0:
            self.current_page_index = 0
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def show_next_page(self):
        # Afficher la page suivante
        self.current_page_index += 1
        if self.current_page_index >= len(self.pages):
            self.current_page_index = len(self.pages) - 1
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def addText(self, page, i):
        layout = QVBoxLayout(page)
        txt = QLabel("Page"+str(i))
        layout.addWidget(txt)

        # Créer une zone de défilement
        scroll_area = QScrollArea(self)
        # Créer un widget à l'intérieur de la zone de défilement
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        # Créer un layout pour le widget à l'intérieur de la zone de défilement
        content_layout = QVBoxLayout(scroll_content)

        if i == 0:
            lbl_title = QLabel("The rules :")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            '''text_browser = QTextBrowser(self)
            text_browser.setPlainText(" A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), "
                "one taking the black stones, the other taking white. The main object of the game is to use your stones to form "
                "territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones "
                "by completely surrounding them. Players take turns, placing one of their stones on a vacant point at each turn,"
                " with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares "
                "and once played stones are not moved. However they may be captured, in which case they are removed from the board, and "
                "kept by the capturing player as prisoners. ")'''
            lbl_txt1 = QLabel(
                " A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), "
                "one taking the black stones, the other taking white. The main object of the game is to use your stones to form "
                "territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones "
                "by completely surrounding them. Players take turns, placing one of their stones on a vacant point at each turn,"
                " with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares "
                "and once played stones are not moved. However they may be captured, in which case they are removed from the board, and "
                "kept by the capturing player as prisoners. ")
            lbl_txt1.setWordWrap(True)
            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictRules.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)
            '''text_browser2 = QTextBrowser(self)
            text_browser2.setPlainText(
                " A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), "
                "one taking the black stones, the other taking white. The main object of the game is to use your stones to form "
                "territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones "
                "by completely surrounding them. Players take turns, placing one of their stones on a vacant point at each turn,"
                " with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares "
                "and once played stones are not moved. However they may be captured, in which case they are removed from the board, and "
                "kept by the capturing player as prisoners. ")'''
            lbl_txt2 = QLabel(
                " A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), "
                "one taking the black stones, the other taking white. The main object of the game is to use your stones to form "
                "territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones "
                "by completely surrounding them. Players take turns, placing one of their stones on a vacant point at each turn,"
                " with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares "
                "and once played stones are not moved. However they may be captured, in which case they are removed from the board, and "
                "kept by the capturing player as prisoners. ")
            lbl_txt2.setWordWrap(True)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt1)
            content_layout.addWidget(lbl_pict)

            content_layout.addWidget(lbl_txt2)

        # Ajouter la zone de défilement au layout principal du QDialog
        layout.addWidget(scroll_area)
        self.go_window = None

    def drawWoodGrainBackground(self, painter):
        # Load a wood texture image
        wood_texture = QPixmap("./icon/woods.jpg")  # Replace with the path to your wood texture image

        # Create a brush with the wood texture
        brush = QBrush(wood_texture)
        painter.fillRect(self.rect(), brush)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)

        self.drawWoodGrainBackground(painter)
        self.update()

    def launchGame(self):
        self.hide()
        if not self.go_window:
            self.go_window = Go()

        self.go_window.show()


