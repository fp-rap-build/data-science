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

from .model import lrmodel

ref = {
    1: 3612, 
    2: 4129, 
    3: 4645, 
    4: 5158, 
    5: 5575,
    6: 5965, 
    7: 6400, 
    8: 6812
  }

log = logging.getLogger(__name__)
router = APIRouter()

df = pd.read_csv('data/hud_requirements - data.csv')

import pandas as pd

zips = pd.read_csv('data/spokane_zipcodes.csv')

zip_set = set(zips['zipcode'])

class DefaultParams(BaseModel):
  """Use this data model to parse the request body JSON."""
  
  zipcode: int = Field(..., example=99203)
  family_members: int = Field(..., example=4)
  monthly_income: int = Field(..., example=2000)

  def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

@router.post('/predict')
def predict(user_input: DefaultParams):
  default_df = user_input.to_df()
  y_pred = lrmodel.predict(default_df)
  return {'qualifies': int(y_pred[0])}

@router.post('/check_eligibility')
def determine_eligibility(zip, family_size, income):
    if zip in zip_set:
        user = zips[zips['zipcode'] == zip]
        user = user[user['family_members'] == family_size]
        user_income = (income * 12)
        comp_income = user['annual_income'].values[0]
    
        if (user_income <= comp_income).all():
            return 'You Qualify!'
        else:
            return 'Sorry, you make too much'
    else:
      return f'Sorry, services not offered in {zip}'


#def predict(user_input):

  #if lrmodel.predict(user_input) == 1:
   #predict = {'predict': 'User does not qualify.'}
    #input.update(predict) 
    #return input
  #else:
    #predict = {'predict':'User qualifies for rental assistance!'}
    #input.update(predict)
    #return input
    

def framemaker(web_in):
  input_frame = pd.DataFrame(web_in, index=[0])
  input_frame = input_frame[['zipcode', 'family_members', 'monthly_income']]
  userinput = input_frame.iloc[[0]]

  return userinput

