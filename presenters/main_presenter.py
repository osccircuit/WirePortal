from presenters.dialog_presenter import DialogPresenter
from views.dialog_view import DialogView
        
class MainPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

    def handle_greet(self):
        name = self.view.entry_name.get_text()
        self.model.name = name

        dialog_view = DialogView()
        dialog_presenter = DialogPresenter(self.model, dialog_view)
        dialog_view.window.present()
