"""Machine learning functions"""

import logging
import random
import numpy as np 
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    zipcode: int = Field(..., example=99205)
    family_size: int = Field(..., example= 4)
    income: int = Field(..., example= 4000)

@router.post('/predict')
async def determine_eligibility(zipcode, family_size, income):

    user = pd.read_csv('data/spokane_zipcodes.csv')


    print(user.head())
    try:
        
        income_goal = user[(user['zipcode'] == zipcode) & (user['family_members'] == family_size)].iloc[0][2] 
        
        zipgoal = user[(user['zipcode'] == zipcode) & (user['family_members'] == family_size)].iloc[0][0] 
        user_income = income * 12
        
        if zip == zipgoal:
            if (user_income <= income_goal):
                return {
                    'SNAP': 0,
                    'CC': 0,
                    'FP': 1
                }
                    
            else:
                return  {
                    'SNAP': 0,
                    'CC': 0,
                    'FP': 0
                }
                    
    except:
        return {
                    'SNAP': 0,
                    'CC': 0,
                    'FP': 1
                }