import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods

class KMeansClustering:

    def __init__(self, file_object, logger_object) -> None:
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self, data):
        self.logger_object.log(self.file_object, 'Elbow Plot Beginning')

        wcss = []

        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            
            plt.plot(range(1, 11), wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of Clusters')
            plt.ylabel('WCSS')
            plt.savefig('preprocessing_data/K-Means_Elbow.png') # Saving the elbow plot

            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction = 'decreasing')
            self.logger_object.log(self.file_object, f'The optimum number of clusters is {self.kn.knee}')

            return self.kn.knee

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception during clustering:: {e}')
            raise Exception

    def create_clusters(self, data, number_of_clusters):

        self.logger_object.log(self.file_object, 'Creating clusters')
        self.data = data

        try:
            self.kmeans = KMeans(n_clusters = number_of_clusters, init = 'k-means++', random_state=42)
            self.y_kmeans = self.kmeans.fit_predict(data)

            self.file_op = file_methods.File_Operation(self.file_object, self.logger_object)

            # Saving KMeans model to directory
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans')

            # Create a new column, to store cluster info
            self.data['Cluster'] = self.y_kmeans

            self.logger_object.log(self.file_object, f'Successfully create {self.kn.knee} clusters.')

        except Exception as e:
            self.logger_object.log(self.file_object, f'Excetion occuring in cluster creation:: {e}')
            raise Exception


