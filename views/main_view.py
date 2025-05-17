from gi.repository import Gtk
class MainView:
    def __init__(self):
        self.presenter = None

        self.window = Gtk.Window(title="WirePortal")
        self.window.set_default_size(400, 250)
        self.window.set_size_request(400, 250)

        # Main Container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # ListBox for ConfFiles
        self.listbox_configs = Gtk.ListBox()
        self.listbox_configs.set_margin_top(10)
        self.listbox_configs.set_margin_start(0)
        self.listbox_configs.set_margin_end(0)
        self.listbox_configs.set_vexpand(True)
        self.listbox_configs.set_hexpand(True)
        self.listbox_configs.props.selection_mode = Gtk.SelectionMode.SINGLE
        self.listbox_configs.props.show_separators = True
        self.scrolled = Gtk.ScrolledWindow(kinetic_scrolling=False)

        # Button for add configs to list
        self.button_list_configs = Gtk.Button(label="List Configs")
        self.button_list_configs.set_valign(Gtk.Align.CENTER)
        self.button_list_configs.set_halign(Gtk.Align.CENTER)
        self.button_list_configs.set_size_request(150, 30)

        # Button to open connection
        self.open_connection_button_text = "Open Connection"
        self.close_connection_button_text = "Close Connection"
        self.button_open_connection = Gtk.Button(
            label=self.open_connection_button_text)
        self.button_open_connection.set_valign(Gtk.Align.START)
        self.button_open_connection.set_halign(Gtk.Align.CENTER)
        self.button_open_connection.set_sensitive(False)
        self.button_open_connection.set_size_request(150, 30)

        self.control_box = Gtk.Box(spacing=10)
        self.control_box.set_margin_start(10)
        self.control_box.set_margin_end(10)
        self.control_box.append(self.scrolled)

        self.control_v_grid = Gtk.Grid(row_spacing=10, margin_top=10)
        self.control_v_grid.attach(self.button_list_configs, 0, 1, 1, 1)
        self.control_v_grid.attach_next_to(
                            self.button_open_connection, 
                            self.button_list_configs,
                            Gtk.PositionType.BOTTOM,
                            1, 1)
        
        self.control_box.append(self.control_v_grid)
        self.main_box.append(self.control_box)
        
        # Status Bar (ActionBar)
        self.status_bar = Gtk.ActionBar()
        self.status_bar.pack_start(Gtk.Label(label="Void"))
        self.main_box.append(self.status_bar)

        self.window.set_child(self.main_box)

        for sig, handler in self.get_signal_handlers().items():
            obj_name, signal_name = sig.rsplit(".", 1)
            if hasattr(self, obj_name):
                obj = getattr(self, obj_name)
                obj.connect(signal_name, handler)

    def show(self, app):
        self.window.set_application(app)
        self.window.present()

    def check_presenter(self):
        if self.presenter is not None:
            return
        self.presenter = getattr(self, "presenter", None)

    def get_signal_handlers(self):
        return {
            "button_list_configs.clicked": self.on_list_configs_clicked,
            "button_open_connection.clicked": self.on_close_open_connection_clicked,
            "listbox_configs.selected_rows_changed": self.on_list_configs_change_selected,
        }

    def on_list_configs_clicked(self, button_list_configs):
        self.check_presenter()
        self.presenter.handle_list_configs()

    def on_close_open_connection_clicked(self, button_open_connection):
        self.check_presenter()
        try:
            if (
                self.button_open_connection.get_label()
                == self.open_connection_button_text
            ):
                result_process = self.presenter.handle_open_connection(
                    self.get_en_label_from_listbox(self.listbox_configs)
                )
                self.button_open_connection.set_label(
                    self.close_connection_button_text)
            elif (
                self.button_open_connection.get_label()
                == self.close_connection_button_text
            ):
                result_process = self.presenter.handle_close_connection()
                self.button_open_connection.set_label(
                    self.open_connection_button_text)
            self.update_status_bar(result_process["message"])
        except Exception as e:
            print(e)

    def on_list_configs_change_selected(self, list_configs):
        self.button_enable(self.button_open_connection)

    def button_disable(self, button):
        if button.is_sensitive():
            button.set_sensitive(False)

    def button_enable(self, button):
        if not button.is_sensitive():
            button.set_sensitive(True)

    def get_en_label_from_listbox(self, listbox):
        try:
            selected_row = listbox.get_selected_row()
            if selected_row is None:
                raise Exception
            return selected_row.get_child().get_first_child().get_text()
        except Exception:
            raise Exception("Row config doesn't selected")

    def clear_list(self):
        self.listbox_configs.remove_all()

    def create_list_scroll_bar(self):
        pass
        # self.listbox_configs.

    def add_list_items(self, conf_files):
        self.clear_list()
        try:
            if len(conf_files) == 0:
                raise Exception
            for conf_file in conf_files:
                row = Gtk.ListBoxRow()
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                box.set_halign(Gtk.Align.START)
                row.set_child(box)
                box.append(Gtk.Label(label=conf_file))
                self.listbox_configs.append(row)
            if self.listbox_configs.get_selected_row() is not None:
                self.button_enable(self.button_open_connection)
        except Exception:
            self.button_disable(self.button_open_connection)

    def update_status_bar(self, new_data):
        start_box = self.status_bar.get_first_child() \
                    .get_first_child().get_first_child()
        end_box = self.status_bar.get_first_child() \
                    .get_last_child().get_first_child()
        for child in start_box:
            self.status_bar.remove(child)
        self.status_bar.pack_start(Gtk.Label(label=str(new_data)))
