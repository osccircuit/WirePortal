class MainPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

    def handle_list_configs(self):
        self.view.add_list_items(self.model.config_model.get_preety_configs())

    def handle_open_connection(self, selected_config):
        self.model.connection_model.set_config_file(selected_config)

        self.model.thread_worker.set_thread_method(
            self.model.connection_model.speed_check
        )
        self.model.thread_worker.set_callback(self.handle_update_speed_label)
        self.model.thread_worker.start()
        return self.model.connection_model.open_connection()

    def handle_close_connection(self):
        self.model.thread_worker.stop()
        self.view.update_speed_label("No Connection")
        return self.model.connection_model.close_connection()

    def handle_update_speed_label(self, speed):
        new_speed_format = " ".join(speed)
        self.view.update_speed_label(new_speed_format)
