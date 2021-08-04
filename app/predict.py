"""Machine learning functions"""

import logging
from os import minor
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

    zipCode: int = Field(..., example = 99205)
    familySize: int = Field(..., example = 4)
    monthlyIncome: int = Field(..., example = 4000)
    unEmp90: int = Field(..., example = 1)
    foodWrkr: int = Field(..., example = 1)
    monthlyRent: int = Field(..., example = 800)
    minorGuest: int = Field(..., example = 1)
    covidFH: int = Field(..., example = 1)


@router.post('/predict')
async def determine_eligibility(zipCode, cityName, familySize, monthlyIncome, monthlyRent, unEmp90, foodWrkr, minorGuest, covidFH):
    if minorGuest == 'true':
        fpNum = 1
    else:
        fpNum = 0

    if covidFH == 'true':
        edpNum = 1
    else:
        edpNum = 0

    
    
    if minorGuest == 'false':
        if unEmp90 == 'false':
            if foodWrkr == 'false':
                if covidFH == 'false':
                    return {
                        'SNAP_ERA': 0,
                        'SNAP_ERAP': 0,
                        'VLP_EDP': edpNum,
                        'FP': fpNum,
                        'LS': 0,
                        'OTHER': 1
                    }
        
    def getIncomegoal(zipCode, familySize):
        income_goal = (user[(user['zipcode'] == int(zipCode)) & (user['family_members'] == int(familySize))].iloc[0][4]).astype(int)
        return income_goal
    try:
        income_goal = getIncomegoal(zipCode, familySize)
    except:
        return{
            'SNAP_ERA': 0,
            'SNAP_ERAP': 0,
            'VLP_EDP': edpNum,
            'FP':fpNum,
            'LS': 0,
            'OTHER': 1
        }
            
    try:
        
        # calculate yearly income from user input of monthly income
        user_income = int(monthlyIncome) * 12
        

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
            

            if int(z) == int(zipCode):
                

                if unEmp90 == 'true':
                    

                    if int(user_income) <= income_goal:
                        
                        if covidFH == 'true':

                            cityName = cityName.lower()
                            if cityName.startswith('spokane'):
                                
                                if cityName.endswith('valley'):
                                    era = 0
                                    erap = 1
                                    fpNum = 0
                                    ls = 0
                                    other = 1
                                else:
                                    era = 1
                                    erap = 0
                                    ls = 1
                                    other = 1
                                    

                                
                            else:
                                era = 1
                                erap = 1
                                fpNum = 0
                                ls = 0
                                other = 1

                        else:
                            era = 0
                            erap = 0
                            fpNum = 0
                            ls = 0
                            other = 1
                    else:
                        era = 0
                        erap = 0
                        fpNum = 0
                        ls = 0
                        other = 1



                else:
                    
                    if int(user_income) <= income_goal:

                        
                        

                        if (int(monthlyRent) / int(monthlyIncome)) >= .50:
                            

                            if covidFH == 'true':
                                cityName = cityName.lower()
                                if cityName.startswith('spokane'):
                                
                                    if cityName.endswith('valley'):
                                        era = 1
                                        erap = 1
                                        fpNum = 0
                                        ls = 0
                                        other = 1
                                    else:
                                        era = 1
                                        erap = 0
                                        ls = 1
                                        other = 1
                                        

                                else:
                                    erap = 1
                                    era = 1
                                    fpNum = 0
                                    ls = 0
                                    other = 1

                            else:
                                erap = 0
                                era = 0
                                fpNum = 0
                                ls = 0
                                other = 1

                        else:
                            erap = 1
                            era = 1
                            ls = 0
                            other = 1
                            

                
                    else:

                        era = 0
                        erap = 0
                        fpNum = 0
                        ls = 0
                        other = 1
                        
        
        return {
            'SNAP_ERAP': 0,
            'SNAP_ERA': 0,
            'VLP_EDP': edpNum,
            'FP':fpNum,
            'LS': ls,
            'OTHER': 1
        }
    except:
        return {

            'SNAP_ERAP': 0,
            'SNAP_ERA': 0,
            'VLP_EDP': edpNum,
            'FP':fpNum,
            'LS': ls,
            'OTHER': 1
        }
