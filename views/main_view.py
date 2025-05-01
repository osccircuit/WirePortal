from gi.repository import Gtk

class MainView:
    def __init__(self):
        self.presenter = None

        self.window = Gtk.Window(title='WirePortal')
        self.window.set_default_size(400, 200)
        self.window.set_size_request(400, 200)

        # Main Container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # ListBox for ConfFiles
        self.listbox_configs = Gtk.ListBox()
        self.listbox_configs.set_margin_top(10)
        self.listbox_configs.set_margin_start(10)
        self.listbox_configs.set_margin_end(10)
        self.listbox_configs.set_vexpand(True)
        self.listbox_configs.props.selection_mode = Gtk.SelectionMode.SINGLE
        self.listbox_configs.props.show_separators = True
        self.main_box.append(self.listbox_configs)

        # Button for add configs to list
        self.button_list_configs = Gtk.Button(label='List Configs')
        self.button_list_configs.set_valign(Gtk.Align.CENTER)
        self.button_list_configs.set_halign(Gtk.Align.CENTER)
        self.button_list_configs.set_margin_top(0)
        self.button_list_configs.set_margin_bottom(10)
        self.main_box.append(self.button_list_configs)

        # Button to open connection
        self.button_open_connection = Gtk.Button(label='Open Connect')
        self.button_open_connection.set_valign(Gtk.Align.START)
        self.button_open_connection.set_halign(Gtk.Align.CENTER)
        self.button_open_connection.set_margin_top(0)
        self.button_open_connection.set_margin_bottom(10)
        self.button_open_connection.set_sensitive(False)
        self.main_box.append(self.button_open_connection)
        

        self.window.set_child(self.main_box)

        for sig, handler in self.get_signal_handlers().items():
            obj_name, signal_name = sig.rsplit('.', 1)
            if hasattr(self, obj_name):
                obj = getattr(self, obj_name)
                obj.connect(signal_name, handler)

    def show(self, app):
        self.window.set_application(app)
        self.window.present()
    
    def check_presenter(self):
        if self.presenter is not None: return
        self.presenter = getattr(self, 'presenter', None)
     
    def get_signal_handlers(self):
        return {
            "button_list_configs.clicked": self.on_list_configs_clicked,
            "button_open_connection.clicked": self.on_open_connection_clicked
        }

    def on_list_configs_clicked(self, button_list_configs):
        self.check_presenter()
        self.presenter.handle_list_configs()
    
    def on_open_connection_clicked(self, button_open_connection):
        self.check_presenter()
        self.presenter.handle_open_connection()

    def button_disable(self, button):
        if button.is_sensitive():
            button.set_sensitive(False)

    def button_enable(self, button):
        if not button.is_sensitive():
            button.set_sensitive(True)

    def clear_list(self):
        self.listbox_configs.remove_all()

    def add_list_items(self, conf_files):
        self.clear_list()
        try:
            if len(conf_files) == 0: raise Exception
            for conf_file in conf_files:
                row = Gtk.ListBoxRow()
                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                box.set_halign(Gtk.Align.START)
                row.set_child(box)
                box.append(Gtk.Label(label=conf_file))
                self.listbox_configs.append(row)
            self.button_enable(self.button_open_connection)
        except Exception:
            self.button_disable(self.button_open_connection)