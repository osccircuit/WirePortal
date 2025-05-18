class MainPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

    def handle_list_configs(self):
        self.view.add_list_items(self.model.config_model.get_preety_configs())

    def handle_open_connection(self, selected_config):
        status_connection = self.model.connection_model.get_connection_status()
        if status_connection["status"] == "connected":
            self.view.update_status_bar(status_connection["message"])
            return

        self.model.connection_model.set_config_file(selected_config)
        status_connection = self.model.connection_model.open_connection()
        self.view.update_status_bar(status_connection["message"])

        if self.model.thread_worker.get_status_run() is not True:
            self.model.thread_worker.set_thread_method(
                self.model.connection_model.speed_check
            )
            self.model.thread_worker.set_callback(self.handle_update_speed_label)
            self.model.thread_worker.start()

    def handle_close_connection(self):
        status_connection = self.model.connection_model.get_connection_status()
        if status_connection["status"] == "disconnect":
            self.view.update_status_bar(status_connection["message"])
            return

        if self.model.thread_worker.get_status_run() is not False:
            self.model.thread_worker.stop()

        status_connection = self.model.connection_model.close_connection()
        self.view.update_status_bar(status_connection["message"])
        self.view.update_speed_label("No Connection")

    def handle_update_speed_label(self, speed):
        new_speed_format = " ".join(speed)
        self.view.update_speed_label(new_speed_format)
