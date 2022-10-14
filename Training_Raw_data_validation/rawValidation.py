from datetime import datetime
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger

class Raw_Data_Validation:
    def __init__(self, path) -> None:
        self.Batch_directory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

    def valuesFromSchema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            file = open('Training_Logs/valuesfromSchemaValidationLog.txt', 'a+')
            message = f'LengthOfDateStampInFile:: {LengthOfDateStampInFile}\tLengthOfTimeStampInFile:: {LengthOfTimeStampInFile}\tNumberofColumns:: {NumberofColumns}\n'
            self.logger.log(file, message)

            file.close()
        
        except ValueError:
            file = open('Training_Logs/valuesfromSchemaValidationLog.txt', 'a+')
            self.logger.log(file, 'ValueError: Value not found inside schema_training.json')
            file.close()
            raise ValueError

        except KeyError:
            file = open('Training_Logs/valuesfromSchemaValidationLog.txt', 'a+')
            self.logger.log(file, 'KeyError: Key value error incorrect key passed')
            file.close()
            raise KeyError

        except Exception as e:
            file = open('Training_Logs/valuesfromSchemaValidationLog.txt', 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def manualRegexCreation(self):
        regex = "['forest_cover_']+[\d_]+[\d]+\.csv"
        return regex

    def createDirectoryGoodBadRawData(self):
        try:
            path = os.path.join('Training_Raw_files_validated/', 'Good_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join('Training_Raw_files_validated/', 'Bad_Raw/')
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as ex:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, f'Error while creating directory {ex}')
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        try:
            path = 'Training_Raw_files_validated/'

            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')

                file = open('Training_Logs/GeneralLog.txt', 'a+')
                self.logger.log(file, 'GoodRaw directory deleted successfully')
                file.close()
        except OSError as ex:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, f'Error while Deleting directory {ex}')
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):
        try:
            path = 'Training_Raw_files_validated/'

            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')

                file = open('Training_Logs/GeneralLog.txt', 'a+')
                self.logger.log(file, 'BadRaw directory deleted before validation')
                file.close()
        except OSError as ex:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, f'Error while Deleting directory {ex}')
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H%M%S')

        try:
            source = 'Training_Raw_files_validated/Bad_Raw/'

            if os.path.isdir(source):
                path = 'TrainingArchiveBadData'

                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = f'{path}/BadData_{date}_{time}'

                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(dest)

                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                
                file = open('Training_Logs/GeneralLog.txt', 'a+')
                self.logger.log(file, 'Bad files moved to archive')

                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                
                self.logger.log(file, 'Bad Raw Data Folder deleted successfully')
                file.close()
            
        except Exception as e:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, f'Error while moving bad files to archive:: {e}')
            file.close()
            raise e

    def validationFileNameRaw(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):

        self.deleteExistingGoodDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()

        self.createDirectoryGoodBadRawData()
        onlyfiles = [f for f in os.listdir(self.Batch_directory)]
        try:
            f = open('Training_Logs/nameValidationLog.txt', 'a+')

            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))

                    if len(splitAtDot[2]) == LengthOfDateStampInFile:
                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:
                            shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Good_Raw')
                            self.logger.log(f, f'Valid filename. File moved to GoodRaw Folder:: {filename}')
                        else:
                            shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Bad_Raw')
                            self.logger.log(f, f'Invalid filename. File moved to BadRaw Folder:: {filename}')
                    else:
                        shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Bad_Raw')
                        self.logger.log(f, f'Invalid filename. File moved to BadRaw Folder:: {filename}')
                else:
                    shutil.copy('Training_Batch_Files/' + filename, 'Training_Raw_files_validated/Bad_Raw')
                    self.logger.log(f, f'Invalid filename. File moved to BadRaw Folder:: {filename}')

        except Exception as e:
            f = open('Training_Logs/nameValidationLog.txt', 'a+')
            self.logger.log(f, f'Error occured validating file name:: {e}')
            f.close()
            raise e

        f.close()

    def validationColumnLength(self, NumberOfColumns):
        try:
            f = open('Training_Logs/columnValidationLog.txt', 'a+')
            self.logger.log(f, 'Column Length validation started!')

            for file in os.listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv('Training_Raw_files_validated/Good_Raw/' + file)

                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move('Training_Raw_files_validated/Good_Raw/' + file, 'Training_Raw_files_validated/Bad_Raw')
                    self.logger.log(f, f'Invalid column length for the file. File moved to Bad Raw Folder :: {file}')
            self.logger.log(f, 'Column Length Validation Completed!')
        except OSError:
            f = open('Training_Logs/columnValidationLog.txt', 'a+')
            self.logger.log(f, f'Error occured while moving the file:: {OSError}')
            f.close()
            raise OSError
        except Exception as e:
            f = open('Training_Logs/columnValidationLog.txt', 'a+')
            self.logger.log(f, f'Error occured:: {e}')
            f.close()
            raise e

        f.close()

    def validateMissingValuesInWholeColumn(self):
        try:
            f = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(f, 'Missing values validation started!')

            for file in os.listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv('Training_Raw_files_validated/Good_Raw/' + file)
                count = 0
                for columns in csv:
                    if(len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move(
                            'Training_Raw_files_validated/Good_Raw/' + file,
                        'Training_Raw_files_validated/Bad_Raw')
                        self.logger.log(f, f'Missing values in the file. File moved to Bad Raw Folder :: {file}')
                        break
                if count == 0:
                    csv.to_csv('Training_Raw_files_validated/Good_Raw/' + file, index=None, header=True)
        except OSError:
            f = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(f, f'Error occured while moving the file:: {OSError}')
            f.close()
            raise OSError
        except Exception as e:
            f = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(f, f'Error occured:: {e}')
            f.close()
            raise e

        f.close()