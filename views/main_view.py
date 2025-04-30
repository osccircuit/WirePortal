from gi.repository import Gtk

class MainView:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("./views/ui_views/main_window.ui")
        self.window = builder.get_object("main_window")
        self.entry_name = builder.get_object("entry_name")
        self.greet_button = builder.get_object("greet_button")

        for sig, handler in self.get_signal_handlers().items():
            obj_name, signal_name = sig.split('.')
            widget = builder.get_object(obj_name)
            widget.connect(signal_name, handler)

    def show(self, app):
        self.window.set_application(app)
        self.window.present()
    
    def get_signal_handlers(self):
        return {
            "greet_button.clicked": self.on_greet_clicked
        }

    def on_greet_clicked(self, button):
        presenter = getattr(self, "presenter", None)
        if presenter:
            presenter.handle_greet()
