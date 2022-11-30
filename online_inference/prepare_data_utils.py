import logging
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@dataclass
class PreparingParams:
    outliers_field: str = field(default='RestingBP')
    nulls_field: str = field(default='Cholesterol')
    target_field: str = field(default='HeartDisease')

@dataclass
class PredictPipelineParams:
    input_data_path: str
    model_path: str
    predict_path: str
    transformer_path: str
    target_col: str
    prepare_params: PreparingParams


def prepare_data(df: pd.DataFrame, params) -> pd.DataFrame:
    logger.info('Preparing dataset...')
    outliers_field = params.outliers_field
    row = df[df[outliers_field] == 0].index
    df = df.drop(df.index[row])

    logger.info('Nulls handling...')
    nulls_field = params.nulls_field
    median_values = df[nulls_field].median()
    row = df[df[nulls_field] == 0].index
    df.loc[row, nulls_field] = median_values

    target_name = params.target_field
    if target_name in df.columns:
        logger.info('Drop target feature...')
        df = df.drop([target_name], axis=1)
    return df


def make_features(transformer: ColumnTransformer, df: pd.DataFrame) -> pd.DataFrame:
    return transformer.transform(df)
