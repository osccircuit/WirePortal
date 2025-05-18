from gi.repository import Gtk, Gio, GLib


class MainView:
    def __init__(self):
        # self.notification_id = "dynamic-notification"

        self.app = None
        self.presenter = None

        # self.window = Gtk.Window(title="WirePortal")
        self.window = Gtk.ApplicationWindow(title="WirePortal")
        self.window.set_default_size(800, 350)
        self.window.set_size_request(800, 350)

        # MenuBar
        self.menu_bar_actions = {}
        # Menu_quit
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda a, p: self.on_window_delete(None))
        self.window.add_action(action)
        self.menu_bar_actions['quit'] = action
        # Menu_RefreshConfs
        action = Gio.SimpleAction.new("refresh_configs", None)
        action.connect("activate", lambda a, p: self.on_list_configs_clicked(None))
        self.window.add_action(action)
        self.menu_bar_actions['refresh_configs'] = action
        # Menu_Connect
        action = Gio.SimpleAction.new("connect", None)
        action.connect(
            "activate", lambda a, p: self.connect()
        )
        self.window.add_action(action)
        action.set_enabled(False)
        self.menu_bar_actions['connect'] = action
        # Menu_Disconnect
        action = Gio.SimpleAction.new("disconnect", None)
        action.connect(
            "activate", lambda a, p: self.disconnect()
        )
        self.window.add_action(action)
        action.set_enabled(False)
        self.menu_bar_actions['disconnect'] = action
        # Menu_About
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda a, p: self.about_window())
        self.window.add_action(action)
        self.menu_bar_actions['about'] = action

        self.header = Gtk.HeaderBar()
        self.header.set_show_title_buttons(True)
        self.menu_btn = Gtk.MenuButton(icon_name="open-menu", tooltip_text="Menu")
        self.popover = Gtk.PopoverMenu()
        self.menu_model = Gio.Menu()

        self.menu_model = Gio.Menu()
        self.section1 = Gio.Menu()
        self.section1.append("Refresh Configs", "win.refresh_configs")
        self.section1.append("Connect", "win.connect")
        self.section1.append("Disconnect", "win.disconnect")

        self.section2 = Gio.Menu()
        self.section2.append("About", "win.about")
        self.section2.append("Quit", "win.quit")

        self.menu_model.append_section(None, self.section1)
        self.menu_model.append_section(None, self.section2)
        self.popover.set_menu_model(self.menu_model)
        self.menu_btn.set_popover(self.popover)
        self.header.pack_end(self.menu_btn)
        self.window.set_titlebar(self.header)

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
        self.scrolled.set_child(self.listbox_configs)

        # Button for add configs to list
        self.button_list_configs = Gtk.Button(label="Refresh Configs")
        self.button_list_configs.set_valign(Gtk.Align.FILL)
        self.button_list_configs.set_halign(Gtk.Align.FILL)
        self.button_list_configs.set_vexpand(True)

        # Button to open connection
        self.open_connection_button_text = "Open Connection"
        self.close_connection_button_text = "Close Connection"
        self.button_open_connection = Gtk.Button(label=self.open_connection_button_text)
        self.button_open_connection.set_valign(Gtk.Align.FILL)
        self.button_open_connection.set_halign(Gtk.Align.FILL)
        self.button_open_connection.set_sensitive(False)
        self.button_open_connection.set_vexpand(True)

        # Speed Label
        self.speed_label = Gtk.Label(label="Speed: No Connection")

        # self.button = Gtk.Button(label="Send notification")

        # Status Bar (ActionBar)
        self.status_bar = Gtk.ActionBar()
        self.status_bar.pack_start(Gtk.Label(label="Void"))

        # Add to container all elements
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
            1,
            1,
        )

        self.control_box.append(self.control_v_grid)
        self.main_box.append(self.control_box)
        self.main_box.append(self.speed_label)
        # self.main_box.append(self.button)
        self.main_box.append(self.status_bar)

        self.window.set_child(self.main_box)

        for sig, handler in self.get_signal_handlers().items():
            obj_name, signal_name = sig.rsplit(".", 1)
            if hasattr(self, obj_name):
                obj = getattr(self, obj_name)
                obj.connect(signal_name, handler)

    def show(self, app):
        self.app = app
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
            "window.close-request": self.on_window_delete,
            # "button.clicked": self.on_notify_clicked,
        }

    def on_list_configs_clicked(self, button_list_configs):
        self.check_presenter()
        self.presenter.handle_list_configs()
        self.button_disable(self.button_open_connection)
        self.menu_bar_actions['connect'].set_enabled(False)
        self.update_status_bar("Scaned Config Directory")

    def on_close_open_connection_clicked(self, button_open_connection):
        self.check_presenter()
        if (
            self.button_open_connection.get_label()
            == self.open_connection_button_text
        ):
            self.connect()
        elif (
            self.button_open_connection.get_label()
            == self.close_connection_button_text
        ):
            self.disconnect()

    def connect(self):
        self.presenter.handle_open_connection(
            self.get_en_label_from_listbox(self.listbox_configs)
        )
        self.button_open_connection.set_label(self.close_connection_button_text)
        self.menu_bar_actions['connect'].set_enabled(False)
        self.menu_bar_actions['disconnect'].set_enabled(True)

    def disconnect(self):
        self.presenter.handle_close_connection()
        self.button_open_connection.set_label(self.open_connection_button_text)
        self.menu_bar_actions['connect'].set_enabled(True)
        self.menu_bar_actions['disconnect'].set_enabled(False)

    def on_list_configs_change_selected(self, list_configs):
        if list_configs.get_selected_row() is not None:
            self.button_enable(self.button_open_connection)
            self.menu_bar_actions['connect'].set_enabled(True)

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
        start_box = (
            self.status_bar.get_first_child().get_first_child().get_first_child()
        )
        end_box = self.status_bar.get_first_child().get_last_child().get_first_child()
        for child in start_box:
            self.status_bar.remove(child)
        self.status_bar.pack_start(Gtk.Label(label=str(new_data)))

    def update_speed_label(self, speed):
        self.speed_label.set_label(f"Speed: {speed}")

    # def on_notify_clicked(self, button):
    #     notification = Gio.Notification.new("Hello")
    #     notification.set_body(
    #         f"Последнее обновление: {GLib.DateTime.new_now_local().format('%H:%M:%S')}"
    #     )
    #     notification.set_priority(Gio.NotificationPriority.HIGH)  # повысим приоритет
    #     notification.add_button("Обновить", "app.update")
    #     notification.add_button("Закрыть", "app.quit")
    #     notification.set_icon(Gio.ThemedIcon.new("D23E_msiexec.0"))
    #     self.app.send_notification(self.notification_id, notification)
    #     GLib.timeout_add_seconds(1, self.on_notify_clicked, button)
    #     return GLib.SOURCE_REMOVE  # Остановить повторение

    def about_window(self):
        self.update_speed_label("ABOUT CALLED")

    def on_window_delete(self, window):
        self.check_presenter()
        self.presenter.handle_close_connection()
        if self.app:
            self.app.quit()
        return False