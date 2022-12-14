import shutil
import sqlite3
import os
import csv
from application_logging.logger import App_Logger

class dbOperations:

    def __init__(self) -> None:
        self.path = 'Training_Database/'
        self.badFilePath = 'Training_Raw_files_validated/Bad_Raw'
        self.goodFilePath = 'Training_Raw_files_validated/Good_Raw'
        self.logger = App_Logger()

    def dataBaseConnection(self, DatabaseName):

        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')

            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, f'Opened {DatabaseName} database successfully')
            file.close()

        except ConnectionError:
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, f'Error while connecting to database: {ConnectionError}')
            file.close()
            raise ConnectionError
        
        return conn

    def createTableDb(self, DatabaseName, column_names):

        try:
            conn = self.dataBaseConnection(DatabaseName)

            c = conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")

            if c.fetchone()[0] == 1:
                conn.close()

                file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
                self.logger.log(file, f'Tables created successfully')
                file.close()

                file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
                self.logger.log(file, f'Closed {DatabaseName} database successfully')
                file.close()

            else:
                for key in column_names.keys():
                    type = column_names[key]

                    try:
                        conn.execute(f"ALTER TABLE Good_Raw_Data ADD COLUMN '{key}' {type}")
                    except:
                        conn.execute(f'CREATE TABLE Good_Raw_Data ({key} {type})')
                
                conn.close()

                file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
                self.logger.log(file, f'Tables created successfully')
                file.close()

                file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
                self.logger.log(file, f'Closed {DatabaseName} database successfully')
                file.close()
        except Exception as e:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, f'Error while creating table: {e}')
            file.close()
            conn.close()
            file = open('Training_Logs/DataBaseConnectionLog.txt', 'a+')
            self.logger.log(file, f'Closed {DatabaseName} database successfully')
            file.close()

            raise e

    def insertIntoTableGoodData(self, Database):

        conn = self.dataBaseConnection(Database)
        goodFilePath = self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in os.listdir(goodFilePath)]
        log_file = open('Training_Logs/DbInsertLog.txt', 'a+')
        count = 1

        for file in onlyfiles:
            try:
                with open(goodFilePath+'/'+file, 'r') as f:
                    next(f)
                    reader = csv.reader(f, delimiter='\n')

                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute(f'INSERT INTO Good_Raw_Data VALUES ({(list_)})')
                                self.logger.log(log_file, f'{file}: File loaded successfully')
                                conn.commit()
                                count += 1
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file, f'Error while creating table: {e}')
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, f'File Moved Successfully {file}')
                log_file.close()
                conn.close()
        
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self, Database):

        self.fileFromDb = 'Training_FileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open('Training_Logs/ExportToCsv.txt', 'a+')

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = 'SELECT * FROM Good_Raw_Data'
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline = ''), delimiter = ',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, 'File exported successfully')
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, f'File exporting failed. Error: {e}')
            log_file.close()