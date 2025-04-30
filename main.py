from gi.repository import Gtk
from models.greeting_model import GreetingModel
from views.main_view import MainView
from presenters.main_presenter import MainPresenter

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.myapp")

    def do_activate(self):
        view = MainView()
        model = GreetingModel()
        presenter = MainPresenter(model, view)
        view.show(self)

    

if __name__ == "__main__":
    app = MyApp()
    app.run(None)