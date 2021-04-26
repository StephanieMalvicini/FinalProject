from PIL import ImageTk, Image

SIZE = (10,10)


class FairnessDefinitionResultImages:

    def __init__(self):
        self.question_mark = ImageTk.PhotoImage(Image.open("images/question_mark.png").resize(SIZE))
        self.failed = ImageTk.PhotoImage(Image.open("images/failed.png").resize(SIZE))
        self.passed = ImageTk.PhotoImage(Image.open("images/passed.png").resize(SIZE))
        self.show_more = ImageTk.PhotoImage(Image.open("images/show_more.png").resize(SIZE))
        self.show_less = ImageTk.PhotoImage(Image.open("images/show_less.png").resize(SIZE))


class GoBackButtonImage:

    def __init__(self):
        self.go_back = ImageTk.PhotoImage(Image.open("images/go_back.png").resize(SIZE))
