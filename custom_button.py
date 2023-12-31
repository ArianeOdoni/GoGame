from PyQt6.QtWidgets import QPushButton


class CustomButton(QPushButton):
    def __init__(self, txt, bg_color=None, fg_color='red'):
        super().__init__()
        self.setText(txt)

        self.fg_style = f"color: {fg_color};" if fg_color else ""

        self.bg_style = f"background-color: {bg_color};"

        self.setStyleSheet(f"QPushButton {{ {self.fg_style} border: 4px solid #A88D75; {self.bg_style} }}")

    def enterEvent(self, event):
        # TODO : choose a good bg color
        self.setStyleSheet(f"QPushButton {{{self.fg_style} border: 4px solid #A88D75; background-color: gray;}}")

    def leaveEvent(self, event):
        self.setStyleSheet(f"QPushButton {{ {self.fg_style} border: 4px solid #A88D75; {self.bg_style} }}")

