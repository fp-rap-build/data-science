"""Machine learning functions"""

import logging
import random
import numpy as np
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()

user = pd.read_csv('app/spokane_zipcodes.csv', header='infer')


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    zipcode: int = Field(..., example = 99205)
    family_size: int = Field(..., example = 4)
    income: int = Field(..., example = 4000)
    unEmp90: str = Field(..., example ='1')
    foodWrkr: str = Field(..., example ='1')
    rent: int = Field(..., example = 800)
    minorGuest: str = Field(..., example = '1')
    covidFH: str = Field(..., example = '1')


@router.post('/predict')
async def determine_eligibility(zipcode, cityName, family_size, income, rent, unEmp90, foodWrkr, minorGuest, covidFH):

    def getIncomegoal(zipcode, family_size):
        income_goal = (user[(user['zipcode'] == int(zipcode)) & (user['family_members'] == int(family_size))].iloc[0][4]).astype(int)
        return income_goal

    income_goal = getIncomegoal(zipcode, family_size)
    
    try:
        # calculate yearly income from user input of monthly income
        user_income = int(income) * 12

        # I know this seems like it can be done a better way
        # we found multiple ways to accomplish this task with
        # more elegant code, but the code didn't translate from
        # a colab notebook to here very well.  Something about
        # the bool values and the way pandas operates in colab
        # versus how it compares in fastAPI.  Not sure exactly
        # what the problem was, but for now this gets our DS API
        # functioning, and thankfully the logic is not very hard to
        # figure out

        # iterate through every zip in Spokane County, on match
        # go to next step in eligibility check
        for z in user['zipcode']:

            if int(z) == int(zipcode):

                if unEmp90 == '1':

                    if int(user_income) <= income_goal:

                        if covidFH == '1':

                            cityName = cityName.lower()
                            if cityName.startswith('spokane'):
                                if cityName.endswith('valley'):
                                    return {
                                        'SNAP_ERA':1,
                                        'SNAP_ERAP': 0,
                                        'CC': 0,
                                        'FP': 0
                                        }
                                else:
                                    pass
                            else:
                                return {
                                    'SNAP_ERA':1,
                                    'SNAP_ERAP': 0,
                                    'CC': 0,
                                    'FP': 0
                                    }
                        else:
                            pass

                    else:
                        pass

                else:

                    if int(user_income) <= income_goal:

                        if (int(rent) / int(income)) >= .50:

                            if covidFH == '1':
                                return {
                                    'SNAP_ERAP': 1,
                                    'SNAP_ERA': 0,
                                    'CC': 0,
                                    'FP': 0
                                    }
                            else:
                                pass

                        else:
                            pass
                    else:
            
            
                        pass
        
                        
        return{
            'SNAP_ERA':0,
            'SNAP_ERAP':0,
            'CC':0,
            'FP':0
        }
    except:
        return {

            'SNAP_ERAP': 0,
            'SNAP_ERA': 0,
            'CC': 0,
            'FP': 0
        }
