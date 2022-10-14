from os import listdir
from application_logging.logger import App_Logger
import pandas as pd

class dataTransform:
    def __init__(self) -> None:
        self.goodDataPath = 'Training_Raw_files_validated/Good_Raw'
        self.logger = App_Logger()

    def addQuotesToStringValuesInColumn(self):
        
        log_file = open('Training_Logs/addQuotesToStringValuesInColumn.txt', 'a+')

        try:
            onlyfiles = [f for f in listdir(self.goodDataPath)]

            for file in onlyfiles:
                data = pd.read_csv(self.goodDataPath + '/' + file)

                data['class'] = data['class'].apply(lambda x: "'" + str(x) + "'")
                data.to_csv(self.goodDataPath + '/' + file, index=None, header=True)
                self.logger.log(log_file, f'{file}: Quotes added successfully!')
        except Exception as e:
            self.logger.log(log_file, f'Data Transformation failed because:: {e}')
            log_file.close()
        
        log_file.close()