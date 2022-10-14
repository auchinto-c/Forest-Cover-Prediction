import pandas as pd

class Data_Getter:

    def __init__(self, file_object, logger_object) -> None:
        self.training_file = 'Training_FileFromDB/InputFile.csv'
        self.file_object = file_object
        self.logger_object = logger_object

    def get_data(self):

        self.logger_object.log(self.file_object, 'Beginning of Data_Getter.get_data()')

        try:
            self.data = pd.read_csv(self.training_file)
            self.logger_object.log(self.file_object, 'Data Load Successful.')
            return self.data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception in getting data:: {e}')
            self.logger_object.log(self.file_object, 'Data Load Unsuccessful.')
            raise Exception