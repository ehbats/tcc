from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath(".."))
from yahoo_data.services.get_ta_indicators import GenerateTechnicalIndicators

class GeneratePCAByGrouping:
    pca = PCA

    def generate_pca(
            self,
            df: pd.DataFrame,
            groupings: dict,
            columns_to_leave: list = []
    ):
        """
        Receives a pandas DataFrame and the name of the columns with which the user wants to group.
        For each group, it runs the PCA leaving one component per group. This returns a DataFrame
        only with the generated components.
        The columns_to_leave param corresponds to any columns the user might want to keep in the DataFrame,
        without this param the code deletes all other columns that were in the DataFrame from the start, as 
        this class's purpose is to reduce the dimensions of the DataFrame.
        """
        reduced_df = pd.DataFrame()
        df = df.dropna()

        for group in groupings:
            group_df = df[group["group_columns"]]
            pca_indicators = PCA(n_components=1)

            reduced_array = pca_indicators.fit_transform(group_df)

            reduced_column = pd.DataFrame(
                data = reduced_array,
                columns = [f'{group["group_name"]}']
            )

            reduced_df[f'{group["group_name"]}'] = reduced_column
        
        if columns_to_leave != []:
            reduced_df = reduced_df.set_index(df.index)
            for column in columns_to_leave:
                reduced_df[column] = df[column]

        return reduced_df
