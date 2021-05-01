from PIL import ImageTk, Image


class FairnessDefinitionResultImages:

    def __init__(self):
        size = (10, 10)
        self.question_mark = ImageTk.PhotoImage(Image.open("images/question_mark.png").resize(size))
        self.failed = ImageTk.PhotoImage(Image.open("images/failed.png").resize(size))
        self.passed = ImageTk.PhotoImage(Image.open("images/passed.png").resize(size))
        self.show_more = ImageTk.PhotoImage(Image.open("images/show_more.png").resize(size))
        self.show_less = ImageTk.PhotoImage(Image.open("images/show_less.png").resize(size))


class MainWindowImages:

    def __init__(self):
        self.go_back = ImageTk.PhotoImage(Image.open("images/go_back.png").resize((15, 15)))
        background_image = Image.open("images/background.png")
        self.background_width, self.background_height = background_image.size
        self.background = ImageTk.PhotoImage(background_image)


class DecisionAlgorithmsEditorImages:

    def __init__(self):
        size = (15, 15)
        self.delete = ImageTk.PhotoImage(Image.open("images/delete.png").resize(size))
        self.add = ImageTk.PhotoImage(Image.open("images/add.png").resize(size))


class LegitimateAttributesImages:

    def __init__(self):
        size = (10, 10)
        self.add = ImageTk.PhotoImage(Image.open("images/add.png").resize(size))
        self.remove = ImageTk.PhotoImage(Image.open("images/remove.png").resize(size))

