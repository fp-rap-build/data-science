"""Machine learning functions"""

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

log = logging.getLogger(__name__)
router = APIRouter()

df = pd.read_csv('data/hud_requirements - data.csv')

@router.post('/predict')
def predict(user_input: Dict):
    user_input = create_df(user_input)
    train, test = train_test_split(df, train_size=0.80, test_size=0.20, 
                                 stratify=df['qualifies'], random_state=42)
    
  # Arrange data into X features matrix and y target vector
  features = ['zipcode', 'family_members', 'monthly_income']
  target = 'qualifies'

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

  return lrmodel

lrmodel = model_maker()

def predict(user_input):

  if lrmodel.predict(user_input) == 1:
    predict = {'predict': 'User does not qualify.'}
    input.update(predict) 
    return input
  else:
    predict = {'predict':'User qualifies for rental assistance!'}
    input.update(predict)
    return input
    }

def framemaker(web_in):
# making dataframe out of dict  
  input_frame = pd.DataFrame(web_in, index=[0])

  input_frame = input_frame[['zipcode', 'family_members', 'monthly_income']]

  userinput = input_frame.iloc[[0]]

  return userinput

  def test():
        input = {
            'zipcode': 99203,
            'family_members': 4,
            'monthly_income': 2000,
        }
        
        user = create_df(input)
        return predict(user)
