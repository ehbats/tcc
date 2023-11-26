from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Dense, LSTM
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
import itertools

class NeuralNetworksWrapper:
    def __init__(self, input_shape):
        optimizer = 'adam'
        self.model = Sequential()
        self.model.add(LSTM(64, input_shape=input_shape))
        self.model.add(Dense(1, input_shape=input_shape))
        self.model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

    def run(self, dataframe: pd.DataFrame, target_column: str, price_column: str, columns_to_drop: list[str] = ['Open', 'High', 'Low', 'Close'], ratio: float = 0.3):

        analysis_df = dataframe.copy(deep = True)
        price_data = self.fetch_original_column_from_df(analysis_df, price_column)
        target_data = self.fetch_original_column_from_df(analysis_df, target_column)

        target_df = analysis_df[target_column]
        target_array = np.array(target_df)

        columns_to_drop.append(target_column)
        features_df = analysis_df.drop(columns=columns_to_drop)
        features_array = np.array(features_df)

        # np.random.seed(31415) 

        min_max_scaler = preprocessing.MinMaxScaler()

        train_features, test_features, train_target, test_target = train_test_split(features_array, target_array, test_size = ratio, shuffle=False)

        # train_features = min_max_scaler.fit_transform(train_features)
        # test_features = min_max_scaler.fit_transform(test_features)
        self.model.fit(train_features, train_target, epochs=10, verbose=0)
        predictions = list(itertools.chain(*self.model.predict(test_features).tolist()))
        errors = abs(predictions - test_target)
        
        start_test_date = dataframe.iloc[len(dataframe.index) - len(test_target)]
        start_test_date = pd.to_datetime(start_test_date.name)

        return {
            'predictions': predictions,
            'errors': errors,
            'test_target': test_target,
            'price_data': price_data,
            'target_data': target_data,
            'start_test_date': start_test_date
        }
    
    def fetch_original_column_from_df(self, analysis_df: pd.DataFrame, price_column: str):
        price_df  = analysis_df[price_column]
        price_array = np.array(price_df)
        price_df = pd.DataFrame({price_column: price_array})
        return price_df