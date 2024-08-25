import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    StandardScaler
    , OneHotEncoder
)
from sklearn.impute import SimpleImputer
import os

wd = os.path.dirname(
    os.path.abspath(__file__)
)

EXAMPLE_DATA = pd.read_csv(
    os.path.join(
        wd, "example_data.csv"
    )
    ,dtype={
        "target": object,
        "checking_account_status": "category",
        "duration": np.float64,
        "credit_history": "category",
        "credit_amount": np.float64,
        "other_installment_plans": "category",
        "job": "category",
        "foreign_worker": "category",
        "interest_rate": np.float64,
        "city": "category",
    }
)

def preprocess_data(data: pd.DataFrame=EXAMPLE_DATA):
    # Split target from features
    y_raw = data['target']
    x_raw = data.drop('target', axis=1)
    
    # Encode target
    unique_labels = sorted(y_raw.unique())
    label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
    y = [label_encoder[label] for label in y_raw]
    
    # Separate column types
    cat_columns = x_raw.select_dtypes(include=['object', 'category']).columns
    num_columns = x_raw.select_dtypes(include=['float64', 'int64']).columns
    
    # Handle categorical data
    cat_cleaner = SimpleImputer(strategy='most_frequent')
    clean_cat_data = pd.DataFrame(
        cat_cleaner.fit_transform(x_raw[cat_columns]),
        columns=cat_columns,
        index=x_raw.index
    )
    
    cat_encoder = OneHotEncoder(drop='first', sparse_output=False)
    encoded_cat_data = pd.DataFrame(
        cat_encoder.fit_transform(clean_cat_data),
        columns=cat_encoder.get_feature_names_out(cat_columns),
        index=x_raw.index
    )
    
    # Handle numerical data
    num_cleaner = SimpleImputer(strategy='median')
    clean_num_data = pd.DataFrame(
        num_cleaner.fit_transform(x_raw[num_columns]),
        columns=num_columns,
        index=x_raw.index
    )
    
    num_scaler = StandardScaler()
    scaled_num_data = pd.DataFrame(
        num_scaler.fit_transform(clean_num_data),
        columns=num_columns,
        index=x_raw.index
    )
    
    # Combine processed data
    X = pd.concat([encoded_cat_data, scaled_num_data], axis=1)
    
    return X, y

test = preprocess_data()
features = test[0]
target = test[1]    
print(features.head())
print(features["foreign_worker_A202"].head())