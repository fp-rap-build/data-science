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
    family_members: int = Field(..., example= 4)
    income: int = Field(..., example= 4000)

@router.post('/predict')
async def determine_eligibility(item: Item):

    zips = pd.read_csv('data/spokane_zipcodes.csv')

    user = zips[zips['zipcode'] == item.zipcode]
    user = user[user['family_members'] == item.family_members]
    user_income = item.income*12
    comp_income = user['annual_income'].astype(np.int32)
        
    if (user_income <= user['annual_income']).all():
        results =  'You Qualify!'
    else:
        results = 'Application Pending - income exceeds limit'

    return {
        'eligibility': results
    }

