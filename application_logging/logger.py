from datetime import datetime

class App_Logger:
    def __init__(self) -> None:
        pass

    def log(self, file_object, log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime('%H:%M:%S')

        file_object.write(f'{self.date}/{self.current_time}\t\t{log_message}\n')