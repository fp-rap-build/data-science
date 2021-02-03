import logging
import random
import pandas as pd
import numpy as np
from fastapi import APIRouter
from typing import Dict
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from category_encoders import OneHotEncoder, OrdinalEncoder

from pydantic import BaseModel, Field, validator

df = pd.read_csv('app/fastapi_data.csv')

features = ['zipcode', 'family_members', 'monthly_income']
target = 'qualifies'

train, test = train_test_split(df, train_size=0.80, test_size=0.20, 
                               stratify=df['qualifies'], random_state=42)

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

lrmodel = Pipeline([
                ('ohe', OneHotEncoder(use_cat_names=True)),
                ('scaler', StandardScaler()),  
                ('impute', SimpleImputer()),
                ('classifier', LogisticRegressionCV())
                ])
lrmodel.fit(X_train, y_train)