from gi.repository import Gtk

class MainView:
    def __init__(self):
        self.window = Gtk.Window(title='WirePortal')
        self.window.set_default_size(400, 200)
        self.window.set_size_request(400, 200)

        # Main Container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # ListBox for ConfFiles
        self.listbox_confs = Gtk.ListBox()
        self.listbox_confs.set_margin_top(10)
        self.listbox_confs.set_margin_start(10)
        self.listbox_confs.set_margin_end(10)
        self.listbox_confs.set_vexpand(True)
        self.listbox_confs.props.selection_mode = Gtk.SelectionMode.SINGLE
        self.listbox_confs.props.show_separators = True
        self.main_box.append(self.listbox_confs)

        # Button for add confs to list
        self.button_list_confs = Gtk.Button(label='List Configs')
        self.button_list_confs.set_valign(Gtk.Align.CENTER)
        self.button_list_confs.set_halign(Gtk.Align.CENTER)
        self.button_list_confs.set_margin_top(0)
        self.button_list_confs.set_margin_bottom(10)
        self.main_box.append(self.button_list_confs)

        self.window.set_child(self.main_box)

        for sig, handler in self.get_signal_handlers().items():
            obj_name, signal_name = sig.rsplit('.', 1)
            if hasattr(self, obj_name):
                obj = getattr(self, obj_name)
                obj.connect(signal_name, handler)

    def show(self, app):
        self.window.set_application(app)
        self.window.present()
    
    def get_signal_handlers(self):
        return {
            "button_list_confs.clicked": self.on_list_confs_clicked
        }

    def on_list_confs_clicked(self, button_list_confs):
        presenter = getattr(self, "presenter", None)
        if presenter:
            presenter.handle_list_confs()

    def clear_list(self):
        self.listbox_confs.remove_all()

    def add_list_items(self, conf_files):
        self.clear_list()
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_halign(Gtk.Align.START)
        row.set_child(box)
        for conf_file in conf_files:
            label = Gtk.Label(label=conf_file)
            box.append(label)
        self.listbox_confs.append(row)