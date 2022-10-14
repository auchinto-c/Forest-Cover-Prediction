from sklearn.model_selection import train_test_split

from data_ingestion import data_loader
from data_preprocessing import preprocessing, clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger

class train_model:
    
    def __init__(self) -> None:
        self.log_writer = logger.App_Logger()
        self.file_object = open('Training_Logs/ModelTrainingLog.txt', 'a+')

    def trainingModel(self):

        # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')

        try:
            # Getting the data from the source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # Data Preprocessing
            # -------------------------------------- #
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)

            data = preprocessor.encodeCategoricalValues(data)

            X = data.drop(['class'], axis = 1)
            Y = data['class']

            X, Y = preprocessor.handleImbalanceDataset(X, Y)

            # Applying the clustering approach
            # -------------------------------------- #
            kmeans = clustering.KMeansClustering(self.file_object, self.log_writer) # Object Initialization
            number_of_clusters = kmeans.elbow_plot(X) # Using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X = kmeans.create_clusters(X, number_of_clusters)

            # Create a new column in the dataset consisting of the corresponding cluster assignments
            X['Labels'] = Y

            # Getting the unique clusters from our dataset
            list_of_clusters = X['Cluster'].unique()

            # Parsing all the clusters and looking for best ML algo for each cluster
            # -------------------------------------- #
            for i in list_of_clusters:
                cluster_data = X[X['Cluster']==i] # Filter the data for one cluster

                # Prepare the feature and label columns
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis = 1)
                cluster_label = cluster_data['Labels']

                # Splitting the data into training and test set for each cluster
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1/3, random_state=355)
                x_train = preprocessor.scaleData(x_train)
                x_test = preprocessor.scaleData(x_test)

                model_finder = tuner.Model_Finder(self.file_object, self.log_writer) # Object Initialization

                # Getting the best model for each of the clusters
                best_model_name, best_model = model_finder.get_best_model(x_train, y_train, x_test, y_test)

                # Saving the best model to the directory
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name+str(i))

            # Logging the Successful Training
            # -------------------------------------- #
            self.log_writer.log(self.file_object, 'Successful End of Training')
            self.file_object.close()
        
        except Exception:
            # Logging the Unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception