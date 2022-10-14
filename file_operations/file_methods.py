import pickle
import os
import shutil

class File_Operations:

    def __init__(self, file_object, logger_object) -> None:
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory = 'models/'

    def save_model(self, model, filename):

        self.logger_object.log(self.file_object, 'Saving the model.')

        try:
            path = os.path.join(self.model_directory, filename)

            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(f'{path}/{filename}.sav', 'wb') as f:
                pickle.dump(model, f) # Save the model to file

            self.logger_object.log(self.file_object, f'Model File {filename} saved.')

            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured while saving the model:: {e}')
            raise Exception

    def load_model(self, filename):

        self.logger_object.log(self.file_object, 'Loading the model.')

        try:
            with open(f'{self.model_directory}{filename}/{filename}.sav', 'rb') as f:
                self.logger_object.log(self.file_object, f'Model File {filename} loaded.')
                return pickle.load(f)
            
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in load_model:: {e}')
            raise Exception

    def find_correct_model_file(self, cluster_number):

        self.logger_object.log(self.file_object, f'Finding current model for the given cluster {cluster_number}')

        try:
            self.cluster_number = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.folder_name)

            for self.file in self.list_of_files:
                try:
                    if self.file.index(str(self.cluster_number)) != -1:
                        self.model_name = self.file
                except:
                    continue
            
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object, f'Returning model name {self.model_name} for Cluster {self.cluster_number}')

            return self.model_name
        
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in finding current model file:: {e}')
            raise Exception