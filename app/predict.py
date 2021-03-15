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
    unEmp90: bool = Field(..., example=True)
    foodWrkr: bool = Field(..., example=True)


@router.get('/predict')
async def determine_eligibility(zipcode, family_size, income, unEmp90, foodWrkr):

    user = pd.read_csv('app/spokane_zipcodes.csv', header='infer')
    
    try:
        allowed_zips = set(user['zipcode'])
        user_income = income * 12
        
        if zipcode in allowed_zips:

            

            income_goal = user[(user['zipcode'] == zipcode) & (user['family_members'] == family_size)]
            print('Found it!')
            print(f'user income: {user_income}')
            income_goal = income_goal['annual_income']
            print(income_goal)
            if (int(user_income) <= int(income_goal)):
                print('made it inside user income statement')

                if unEmp90 == True:
                    return {
                        'SNAP': 1,
                        'CC': 0,
                        'FP': 0
                }

            
            else:
                return {
                    'SNAP': 0,
                    'CC': 0,
                    'FP': 1
                }
    except:
        return f"Sorry, we don't offer services in {zip} yet, please contact yo momma"