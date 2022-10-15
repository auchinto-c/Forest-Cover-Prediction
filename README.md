# Forest-Cover-Prediction

## Introduction
<hr>
This project aims to predict the type of forest cover given a set of features. The features are based on data collected as part of previous years of survey. This is a **Multi-Class Classification** problem solved using models based on **Random Forest Classifier** and **XGBoost Classifier**.
<br><br>

## Credits
<hr>

|                   | Details |
|-------------------|---------------------------------|
| **Tutorial/Code** | iNeuron - FSDS - Training       |

## Data Description
<hr>

### Target

- **Class**: Various forest types. The values are as follows:
  - Lodgepole_Pine
  - Spruce_Fir
  - Douglas_fir
  - Krummholz
  - Ponderosa_Pine
  - Aspen
  - Cottonwood_Willow

### Features

These features are relative to a point where the survey is being conducted.
1. **Elevation**: Height of the point from mean sea level.
2. **Aspect**: Angle of point relative to a celestial body (Here, Sun).
3. **Slope**: Slope of the land at this point. This governs factors like water retention and root strength.
4. **Horizontal Distance to Water body**
5. **Vertical Distance to Water body**
6. **Horizontal Distance to Roadways**
7. **Horizontal Distance to Fire Points**
8. **Wilderness**: This is classified into 4 types (Area1, Area2, Area3 and Area4)
9.  **Soil Types**: This is classified into 40 types, labeled from 1 to 40.
    
## Brief
<hr>

|           | **Version** | **Details**                                  |
|-----------|-------------|----------------------------------------------|
| **Model** | v1          | Random Forest Classifier, XGBoost Classifier                     |

## Basic Code Flow
<hr>

1. Data Ingestion
2. Data Preprocessing
3. Model Selection
4. Model Tuning
5. Prediction
6. Logging Framework
7. Deployment

## Architecture
<hr>

![img](https://github.com/auchinto-c/Forest-Cover-Prediction/blob/main/ml_lifecycle.png)

1. **Data Ingestion** for Training
   1. Client providing the access to data available in shared hosting
   2. Data(Batches) for training
   3. Data Validation - This is done in reference to Schema provided by the client as per the SLA.
      1. Validating whether the data file names are in proper format
      2. Validating Column Length
      3. Validating Missing values in whole column
   4. Data Transformations
   5. Data insertion in database - To have a single repository of transformed validated data
   6. Exporting data from database to CSV for training
2. **Data Preprocessing**
3. **Data Clustering** - Obtaining the optimal number of clusters from the training dataset, using elbow plot
4.  **Model Selection and Training**
    1.  Getting the best model for each cluster
    2.  Hyperparameter Tuning for each model
    3.  Model saving
5.  **Cloud Deployment**
    1.  Cloud Setup
    2.  Pushing the app to cloud
    3.  Application start
6.  **Data Ingestion for Prediction**
    1.  Data from client for prediction
    2.  Data Validation (similar)
    3.  Data Transformation
    4.  Data insertion in databases
    5.  Export data from database to CSV for prediction
7.  **Data Preprocessing**
8.  **Data Clustering**
9.  **Predictions**
    1.  Model call for specific cluster
    2.  Prediction
    3.  Export predictions to CSV

## Library and Tools
<hr>

### Language
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML 5](https://img.shields.io/badge/html-%23323330.svg?style=for-the-badge&logo=html5&logoColor=%23F7DF1E)

### Data Analysis
![pandas](https://img.shields.io/badge/pandas-%23281f4f.svg?style=for-the-badge&logoColor=white)
![numpy](https://img.shields.io/badge/numpy-%23548ecc.svg?style=for-the-badge&logoColor=white)

### Model Development
![scikit-learn](https://img.shields.io/badge/scikit-learn-%23cc8854.svg?style=for-the-badge&logoColor=white)
![imblearn](https://img.shields.io/badge/scikit-learn-%23cc8854.svg?style=for-the-badge&logoColor=white)
![xgboost](https://img.shields.io/badge/scikit-learn-%23cc8854.svg?style=for-the-badge&logoColor=white)

### Visualizations
![matplotlib](https://img.shields.io/badge/matplotlib-%230e4e5e.svg?style=for-the-badge&logoColor=white)

### Model Serialisation
![pickle](https://img.shields.io/badge/pickle-%23634f0c.svg?style=for-the-badge&logoColor=white)

### Web Framework
![Flask](https://img.shields.io/badge/Flask-%23154718.svg?style=for-the-badge&logo=flask&logoColor=white)

### Deployment
![Heroku](https://img.shields.io/badge/heroku-%23a65dba.svg?style=for-the-badge&logo=heroku&logoColor=white)
<br><br>

## Visualizations
<hr>

![img](https://github.com/auchinto-c/Forest-Cover-Prediction/blob/main/preprocessing_data/K-Means_Elbow.png)

**Conclusion** - 4 clusters identified