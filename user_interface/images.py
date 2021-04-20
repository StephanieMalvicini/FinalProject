from PIL import ImageTk, Image

SIZE = (10,10)


class Images:

    def __init__(self):
        self.question_mark = ImageTk.PhotoImage(Image.open("images/question_mark.png").resize(SIZE))
        self.failed = ImageTk.PhotoImage(Image.open("images/failed.png").resize(SIZE))
        self.passed = ImageTk.PhotoImage(Image.open("images/passed.png").resize(SIZE))
