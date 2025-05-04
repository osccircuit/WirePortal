from presenters.dialog_presenter import DialogPresenter
from views.dialog_view import DialogView
from gi.repository import Gtk


class MainPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

    def handle_list_configs(self):
        self.view.add_list_items(self.model.get_preety_configs())

    def handle_open_connection(self, selected_config):
        return self.model.run_connect_command(selected_config)

    def handle_close_connection(self):
        return self.model.run_disconnect_command()
