from gi.repository import Gtk

class DialogView:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("./views/ui_views/about_window.ui")
        self.window = builder.get_object("about_window")
        self.label_greeting = builder.get_object("label_greeting")
        # self.close_button = builder.get_object("close_button")

        # for sig, handler in self.get_signal_handlers().items():
        #     obj_name, signal_name = sig.split('.')
        #     widget = builder.get_object(obj_name)
        #     widget.connect(signal_name, handler)

    # def get_signal_handlers(self):
    #     return {
    #         "close_button.clicked": self.on_close_clicked
    #     }

    def on_close_clicked(self, button):
        self.window.destroy()
