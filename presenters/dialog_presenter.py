
class DialogPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self
        # greeting = f"Привет, {self.model.name}!"
        # self.view.label_greeting.set_text(greeting)
