import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from models.model import Model
from views.main_view import MainView
from presenters.main_presenter import MainPresenter


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.myapp")

    def do_activate(self):
        view = MainView()
        model = Model()
        MainPresenter(model, view)
        view.show(self)


if __name__ == "__main__":
    app = MyApp()
    app.run(None)
