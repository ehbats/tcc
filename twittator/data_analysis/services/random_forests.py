
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

class RandomForestsWrapper:
    """
    This wrapper applies the Random Forests Regressor
    to a stock prices DataFrame. Because this is a very repetitive process,
    this class is useful to avoid lots of code.
    """
    def run(self, dataframe: pd.DataFrame, target_column: str):

        analysis_df = dataframe.copy(deep = True)

        target_df = analysis_df[target_column]
        target_array = np.array(target_df)

        features_df = analysis_df.drop(columns=target_column)
        features_array = np.array(features_df)

        np.random.seed(31415) 

        min_max_scaler = preprocessing.MinMaxScaler()

        train_features, test_features, train_target, test_target = train_test_split(features_array, target_array, test_size = 0.3)

        train_features = min_max_scaler.fit_transform(train_features)
        test_features = min_max_scaler.fit_transform(test_features)
        random_forests_intance = RandomForestRegressor(random_state=0)
        random_forests_intance.fit(train_features, train_target)
        predictions = random_forests_intance.predict(test_features)
        errors = abs(predictions - test_target)
        
        return {
            'predictions': predictions,
            'errors': errors,
            'test_target': test_target
        }