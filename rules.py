from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QBrush, QPainter
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QStackedWidget, QWidget, QLabel, QHBoxLayout, \
    QScrollArea, QGridLayout
from custom_button import CustomButton as button


class Rules(QDialog):
    def __init__(self):
        super().__init__()
        self.go_window = None
        self.stacked_widget = None
        self.current_page_index = 0
        self.btn_next = button("")
        self.btn_previous = button("")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Menu')
        self.setGeometry(200, 200, 800, 600)

        # QDialog Layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Espace extensible à gauche
        passBtn = button('Return to the game', 'rgb(221,221,221)', 'rgb(0,0,0)')
        passBtn.setFixedSize(150, 25)
        top_layout.addWidget(passBtn)
        main_layout.addLayout(top_layout)

        passBtn.clicked.connect(self.returnToGame)

        # Create a Satcked to have all the page at the same place
        self.stacked_widget = QStackedWidget(self)

        # Créer les pages et les ajouter au widget empilable
        self.pages = []
        for i in range(6):
            page = QWidget(self)
            self.addText(page, i)
            self.pages.append(page)
            self.stacked_widget.addWidget(page)

        # Ajouter le widget empilable au layout principal
        main_layout.addWidget(self.stacked_widget)

        # Ajouter des boutons de navigation (Next et Previous)
        nav_layout = QHBoxLayout()
        main_layout.addLayout(nav_layout)

        self.btn_previous = button('Previous', 'rgb(221,221,221)')
        self.btn_previous.clicked.connect(self.show_previous_page)
        nav_layout.addWidget(self.btn_previous)

        self.btn_next = button('Next', "rgb(221,221,221)")
        self.btn_next.clicked.connect(self.show_next_page)
        nav_layout.addWidget(self.btn_next)

        # Afficher la première page par défaut
        self.current_page_index = 0
        self.btn_previous.setVisible(False)
        self.stacked_widget.setCurrentIndex(self.current_page_index)
        self.show()

    def show_previous_page(self):
        self.btn_next.setText("Next")
        # Afficher la page précédente
        self.current_page_index -= 1
        if self.current_page_index < 0:
            self.current_page_index = 0
        if self.current_page_index == 0:
            self.btn_previous.setVisible(False)
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def show_next_page(self):
        self.btn_previous.setVisible(True)
        # show next page
        self.current_page_index += 1
        if self.current_page_index >= len(self.pages):
            self.returnToGame()
            self.current_page_index = len(self.pages) - 1
        if self.current_page_index == len(self.pages)-1:
            self.btn_next.setText("Return to the game")
        self.stacked_widget.setCurrentIndex(self.current_page_index)

    def addText(self, page, i):
        layout = QVBoxLayout(page)

        # Créer une zone de défilement
        scroll_area = QScrollArea(self)
        # Créer un widget à l'intérieur de la zone de défilement
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        # Créer un layout pour le widget à l'intérieur de la zone de défilement
        content_layout = QVBoxLayout(scroll_content)

        if i == 0:
            lbl_title = QLabel("The rules:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            '''lbl_txt1 = QLabel(
                " A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces (called stones), "
                "one taking the black stones, the other taking white. The main object of the game is to use your stones to form "
                "territories by surrounding vacant areas of the board. It is also possible to capture your opponent's stones "
                "by completely surrounding them. Players take turns, placing one of their stones on a vacant point at each turn,"
                " with Black playing first. Note that stones are placed on the intersections of the lines rather than in the squares "
                "and once played stones are not moved. However they may be captured, in which case they are removed from the board, and "
                "kept by the capturing player as prisoners. ")'''
            lbl_txt1 = QLabel("\nA game of Go starts with an empty board.\n"
                              "\nEach player has an effectively unlimited supply of pieces, called stones:\n"
                              "\t- one taking the black stones (first player)\n"
                              "\t- the other taking white\n"
                              "\nThe Main object of the game: \n"
                              "\t- use your stones to form territories -> surrounding vacant areas of the board. \n"
                              "\t- capture your opponent's stones by completely surrounding them.\n"
                              "\nPlayers take turns, placing one of their stones on a vacant point at each turn.\n"
                              "\nNote:\n "
                              "\t- stones are placed on the intersections of the lines rather than in the squares.\n"
                              "\t- once played stones are not moved.\n"
                              "\t- stones may be captured, in which case they are removed from the board, and kept by the capturing player as "
                              "prisoners.\n"
                              "\nAt the end of the game, the players keep score:\n"
                              "\t- one point for each vacant point inside their own territory \n"
                              "\t- one point for every stone they have captured.\n "
                              "  -> The player with the larger total of territory plus prisoners is the winner.")
            lbl_txt1.setWordWrap(True)
            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictRules.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)
            '''lbl_txt2 = QLabel("Diagram 1 shows the position at "
                              "the end of a game on a 9 by 9 board, during which Black captured one white stone at "
                              "a.Black has surrounded 15 points of territory, 10 in the lower right corner and 5 "
                              "towards the top of the board. Black's territory includes the point a formerly occupied "
                              "by the white stone Black has captured. Adding this prisoner, Black has a total of 16 "
                              "points.White's territory is 17 points, so White wins the game by one point")'''
            lbl_txt2 = QLabel("The diagram shows the position at the end of a game on a 9 by 9 board, during which "
                              "Black captured one white stone at a. \n"
                              "Black has surrounded 1 point for white stone captured and 15 points of territory\n"
                              "\t- 10 in the lower right corner \n"
                              "\t- 5 towards the top of the board.\n"
                              "Black has a total of 16 points.\n"
                              "White's territory is 17 points. -> White wins the game by one point")
            lbl_txt2.setWordWrap(True)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt1)
            content_layout.addWidget(lbl_pict)

            content_layout.addWidget(lbl_txt2)

        if i == 1:
            lbl_title = QLabel("Capturing stones and counting liberties:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt1 = QLabel("Liberties:\n"
                              "\t - the empty points which are horizontally and vertically adjacent to a stone\n"
                              "\t- a solidly connected string of stones\n"
                              "\nAn isolated stone or solidly connected string of stones is captured "
                              "when all of its liberties are occupied by enemy stones.")
            lbl_txt1.setWordWrap(True)
            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt1)

            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictLib1.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt2 = QLabel("This diagram shows three isolated white stones with their liberties, marked by "
                              "crosses.\n"
                              "Stones which are on the edge of the board have fewer liberties than those in the "
                              "centre of the board.\n"
                              "A single stone has :\n"
                              "\t- has 3 liberties on the side.\n"
                              "\t- only two liberties on a corner.")
            lbl_txt2.setWordWrap(True)

            lbl_pict2 = QLabel(self)
            lbl_pict2.setPixmap(QPixmap("./icon/pictLib2.jpg"))
            lbl_pict2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt3 = QLabel("This diagram shows the same three stones of first diagram each with only one liberty "
                              "left and therefore subject to capture on Black's next turn. \n"
                              "Each of these white stones is said to be in atari -> they are about to be captured. ")
            lbl_txt3.setWordWrap(True)

            lbl_pict3 = QLabel(self)
            lbl_pict3.setPixmap(QPixmap("./icon/pictLib3.jpg"))
            lbl_pict3.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt4 = QLabel("This diagram shows the position which would arise if "
                              "Black went on to play at b in the previous diagram. \n"
                              "Black has taken the captured stone from the board, "
                              "and in a real game would keep it as a prisoner.\n"
                              "The same remarks would apply to the other two white stones, should Black play "
                              "at c or d.")
            lbl_txt4.setWordWrap(True)

            image_widget = QWidget()
            image_text_layout = QGridLayout(image_widget)
            image_text_layout.addWidget(lbl_pict, 0, 0)
            image_text_layout.addWidget(lbl_pict2, 0, 1)
            image_text_layout.addWidget(lbl_pict3, 0, 2)
            image_text_layout.addWidget(lbl_txt2, 1, 0)
            image_text_layout.addWidget(lbl_txt3, 1, 1)
            image_text_layout.addWidget(lbl_txt4, 1, 2)

            content_layout.addWidget(image_widget)

        if i == 2:
            lbl_title = QLabel("Strings:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt1 = QLabel("Solidly connected string is made of stones occupying adjacent points "
                              "(horizontally or vertically adjacent, no diagonals).")
            lbl_txt1.setWordWrap(True)

            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictString1.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt2 = QLabel("This diagram shows 2 solidly connected strings of stones,the two marked black stones "
                              "in the top left of th diagram are two separate strings, not a single one.")
            lbl_txt2.setWordWrap(True)

            # capturing strings
            lbl_title2 = QLabel("\nCapturing strings:")
            lbl_title2.setStyleSheet("font-weight: bold;""font-size: 16px;")

            lbl_txt3 = QLabel("As far as capturing is concerned, a string of stones is treated as a single unit. As "
                              "with isolated stones, a string is captured when all of its liberties are occupied by "
                              "enemy stones")
            lbl_txt3.setWordWrap(True)

            lbl_pict2 = QLabel(self)
            lbl_pict2.setPixmap(QPixmap("./icon/pictString2.jpg"))
            lbl_pict2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt4 = QLabel("In this diagram: the strings of thetop diagram have both been reduced to just one "
                              "liberty. \nNote: \n\t- The black string in the top right is not yet captured because of "
                              "the internal liberty at f.\n\t- The two stones at the top left of the diagram can each be "
                              "captured independently at g or h. ")
            lbl_txt4.setWordWrap(True)

            lbl_pict3 = QLabel(self)
            lbl_pict3.setPixmap(QPixmap("./icon/pictString3.jpg"))
            lbl_pict3.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt5 = QLabel("In the diagram we see the position which would result if:\n\t- Black captured at e and "
                              "\n\t- White captured at f and at g. \nThe remaining black stone could be captured at h. "
                              "\n\nAs with the capture of a single stone, the points formerly occupied by the black string "
                              "have become white territory, and vice versa. ")
            lbl_txt5.setWordWrap(True)

            lbl_title3 = QLabel("\nSelf-Capture:")
            lbl_title3.setStyleSheet("font-weight: bold;""font-size: 16px;")
            lbl_txt6 = QLabel("A player may not self-capture, that is play a stone into a position where it would have "
                              "no liberties or form part of a string which would thereby have no liberties, unless, "
                              "as a result, one or more of the stones surrounding it is captured. ")
            lbl_txt6.setWordWrap(True)

            lbl_pict4 = QLabel(self)
            lbl_pict4.setPixmap(QPixmap("./icon/pictString4.jpg"))
            lbl_pict4.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt7 = QLabel("In this diagram, White may not play at i or j:"
                              " since either of these plays would be self-capture -> the stones would then have "
                              "no liberties.")
            lbl_txt7.setWordWrap(True)

            lbl_pict5 = QLabel(self)
            lbl_pict5.setPixmap(QPixmap("./icon/pictString5.jpg"))
            lbl_pict5.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_txt8 = QLabel("In this diagram the outside liberties have been filled. \nThe plays at i and j become "
                              "legal: they fill the last black liberty in each case, "
                              "and the black stones being captured "
                              "and removed from the board as White's prisoners.")
            lbl_txt8.setWordWrap(True)

            image_widget = QWidget()
            image_text_layout = QGridLayout(image_widget)
            image_text_layout.addWidget(lbl_pict2, 0, 0)
            image_text_layout.addWidget(lbl_pict3, 0, 1)
            image_text_layout.addWidget(lbl_txt4, 1, 0)
            image_text_layout.addWidget(lbl_txt5, 1, 1)

            image_widget2 = QWidget()
            image_text_layout2 = QGridLayout(image_widget2)
            image_text_layout2.addWidget(lbl_pict4, 3, 0)
            image_text_layout2.addWidget(lbl_pict5, 3, 1)
            image_text_layout2.addWidget(lbl_txt7, 4, 0)
            image_text_layout2.addWidget(lbl_txt8, 4, 1)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt1)
            content_layout.addWidget(lbl_pict)
            content_layout.addWidget(lbl_txt2)
            content_layout.addWidget(lbl_title2)
            content_layout.addWidget(lbl_txt3)

            content_layout.addWidget(image_widget)
            content_layout.addWidget(lbl_title3)
            content_layout.addWidget(lbl_txt6)

            content_layout.addWidget(image_widget2)

        if i == 3:
            lbl_title = QLabel("Life and death and the concept of eyes:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt1 = QLabel("Any string or group of stones which has two or more eyes is permanently safe from "
                              "capture and is referred to as a live string or live group. "
                              "\nConversely, a string of stones which is unable to make two eyes, and is cut off and "
                              "surrounded by live enemy strings, is called a dead string since it is hopeless and "
                              "unable to avoid eventual capture.")
            lbl_txt1.setWordWrap(True)

            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictLife1.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt2 = QLabel("The black string here could only be captured if White were able to play at both m and n."
                              "Since the first of these plays would be self-capture, there is no way that White can "
                              "carry out the capture. These two separate spaces within the group are known as eyes. ")
            lbl_txt2.setWordWrap(True)

            lbl_pict2 = QLabel(self)
            lbl_pict2.setPixmap(QPixmap("./icon/pictLife2.jpg"))
            lbl_pict2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt3 = QLabel("In this diagram, the black string at the bottom is in danger of being captured."
                              "\nTo ensure that Black's string has two eyes, Black needs to play at o. "
                              "\nIf White plays at o, the black string will no longer be able to make two eyes, and "
                              "cannot avoid eventual capture; White can always fill in the outside liberties and then "
                              "play at p and at q. Black plays at p or q would only hasten the string's death.The black"
                              " string at the top left of Diagram 11 is already alive even though there is a White "
                              "stone inside one of its eyes. "
                              "\nSince White can never capture the black stones, the White"
                              "stone caught inside the string cannot be saved.")
            lbl_txt3.setWordWrap(True)

            lbl_txt4 = QLabel("Players are not obliged to complete the capture of an isolated dead string once it is "
                              "clear to both players that the string is dead \n\t-> this is a hopeless string. "
                              "\nIn the previous diagram, once White has played at o, the situation may be left as it "
                              "is until the end of the game. Then, the hopeless strings are simply removed from the "
                              "board and counted together with the capturing player's other prisoners.  ")
            lbl_txt4.setWordWrap(True)

            image_widget = QWidget()
            image_text_layout = QGridLayout(image_widget)
            image_text_layout.addWidget(lbl_pict, 0, 0)
            image_text_layout.addWidget(lbl_pict2, 0, 1)
            image_text_layout.addWidget(lbl_txt2, 1, 0)
            image_text_layout.addWidget(lbl_txt3, 1, 1)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt1)
            content_layout.addWidget(image_widget)
            content_layout.addWidget(lbl_txt4)

        if i == 4:
            lbl_title = QLabel("The ko rule:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt = QLabel("The ko rule removes this possibility of indefinite repetition by forbidding the "
                             "recapture of the ko,")
            lbl_txt.setWordWrap(True)

            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictKO1.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt1 = QLabel("At the top of this diagram, Black can capture a stone by playing at r. "
                              "\nThis results in the situation at the top of the bellow diagram."
                              "\nHowever, this stone is itself vulnerable to capture by a White play at u in the below "
                              "diagram. "
                              "\nIf White were allowed to recapture immediately at u, the position would revert to that"
                              "in top diagram, and there would be nothing to prevent this capture and recapture "
                              "continuing indefinitely. This pattern of stones is called ko - a Japanese term meaning "
                              "eternity. Two other possible shapes for a ko, on the edge of the board and in the corner"
                              ", are also shown in this diagram. ")
            lbl_txt1.setWordWrap(True)

            lbl_pict2 = QLabel(self)
            lbl_pict2.setPixmap(QPixmap("./icon/pictKO2.jpg"))
            lbl_pict2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_txt2 = QLabel("In this case a play at u in this diagram, until White has made at least one play "
                              "elsewhere. "
                              "\nBlack may then fill the ko, but if Black chooses not to do so, instead answering "
                              "White's intervening turn elsewhere, White is then permitted to retake the ko."
                              "\nSimilar remarks apply to the other two positions in these diagrams:"
                              "\nthe corresponding plays at w and v in this diagram must also be delayed by one turn. ")
            lbl_txt2.setWordWrap(True)

            lbl_title2 = QLabel("Seki:")
            lbl_title2.setStyleSheet("font-weight: bold;""font-size: 16px;")
            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt3 = QLabel(
                "Usually a string which cannot make two eyes will die unless one of the surrounding enemy "
                "strings also lacks two eyes. "
                "\nThis often leads to a race to capture, but can also result in a stand-off situation, "
                "known as seki, in which neither string has two eyes, but neither can capture the other "
                "due to a shortage of liberties. Two examples of seki are shown in the previous Diagram. "
                "\nNeither player can afford to play at x, y or z, since to do so would enable the other "
                "to make a capture. ")
            lbl_txt3.setWordWrap(True)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_txt)
            content_layout.addWidget(lbl_pict)
            content_layout.addWidget(lbl_txt1)
            content_layout.addWidget(lbl_pict2)
            content_layout.addWidget(lbl_txt2)
            content_layout.addWidget(lbl_title2)
            content_layout.addWidget(lbl_txt3)

        if i == 5:
            lbl_title = QLabel("The end of the game:")
            lbl_title.setStyleSheet("font-weight: bold;""font-size: 16px;")

            lbl_pict = QLabel(self)
            lbl_pict.setPixmap(QPixmap("./icon/pictEnd1.jpg"))
            lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Ajouter du contenu au widget à l'intérieur de la zone de défilement
            lbl_txt = QLabel("When you think your territories are all safe, you can't:"
                             "\n\t- gain any more territory"
                             "\n\t- reduce your opponent's territory "
                             "\n\t- capture more strings"
                             "\nInstead of playing a stone on the board you pass and hand a stone to your opponent "
                             "as a prisoner."
                             "\n => Two consecutive passes ends the game. \n"
                             "\nAny hopeless strings are removed and become prisoners. "
                             "\nIf you cannot agree whether a string is dead or not, then continue playing; "
                             "you can then complete capture of disputed strings or confirm they are alive. "
                             "(Playing during a continuation does not change the score as each play is the "
                             "same as a pass.) Since Black played first, White must play last and may need to make "
                             "a further pass. ")
            lbl_txt.setWordWrap(True)

            content_layout.addWidget(lbl_title)
            content_layout.addWidget(lbl_pict)
            content_layout.addWidget(lbl_txt)

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

    def returnToGame(self):
        self.hide()

