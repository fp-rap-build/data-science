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

# temp turn off apps
# to do: make back door
# another change for push

@router.post('/predict')
async def determine_eligibility(zipCode, cityName, familySize, monthlyIncome, monthlyRent, unEmp90, foodWrkr, minorGuest, covidFH, qualifiedForUnemployment, proofOfRisk):
    

    # check if household has marked any of the covidFH questions (one or more makes mergedCovidFH = 1)
    if (covidFH == 'true' or qualifiedForUnemployment == 'true' or proofOfRisk == 'true'):
        mergedCovidFH = 'true'
    else:
        mergedCovidFH = 'false'

    # if they have any impact by covid, they qualify for eviction defense program
    if mergedCovidFH  == 'true':
        edpNum = 1
    else:
        edpNum = 0

    
    # check for edge case where they don't meet any of the criteria for eligibility
    # (still point them to other resources so not all hope is lost)
    if minorGuest == 'false':
        if unEmp90 == 'false':
            if foodWrkr == 'false':
                if mergedCovidFH == 'false':
                    return {
                        'SNAP_ERA': 0,
                        'SNAP_ERAP': 0,
                        'VLP_EDP': 0,
                        'FP': 0,
                        'LS': 0,
                        'OTHER': 1
                    }
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        pass

    #  use family size and zipcode to determine the max they can earn yearly and still qualify 
    def getIncomegoal(zipCode, familySize):
        income_goal = (user[(user['zipcode'] == int(zipCode)) & (user['family_members'] == int(familySize))].iloc[0][4]).astype(int)
        return income_goal
    try:
        # attempt to get income goal, will only work for families inside spokane county
        income_goal = getIncomegoal(zipCode, familySize)
    except:
        # if the zipcode was outside of spokane county, they don't qualify for help from any of us
        return{
            'SNAP_ERA': 0,
            'SNAP_ERAP': 0,
            'VLP_EDP': 0,
            'FP':0,
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
                print('found zipcode')

                if unEmp90 == 'true':
                    

                    if int(user_income) <= income_goal:
                        
                        if mergedCovidFH == 'true':

                            cityName = cityName.lower()
                            if cityName == 'spokane':
                                era = 1
                                ls = 1
                                # temp disabled
                                fpNum = 0
                                erap = 0
                                other = 1
                            else:
                                era = 0
                                ls = 0
                                fpNum = 0
                                erap = 1
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
                            

                            if mergedCovidFH == 'true':
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
                                    erap = 1
                                    era = 0
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
                            if mergedCovidFH == 'true':
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
                                    erap = 1
                                    era = 0
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

                        era = 0
                        erap = 0
                        fpNum = 0
                        ls = 0
                        other = 1
                        
        # check if household has a minor
        if minorGuest == 'true':
            cityName = cityName.lower()
            if cityName.startswith('spokane'):
                if cityName.endswith('valley'):
                    fpNum = 0
                else:
                    # temp disabled
                    fpNum = 0
            else:
                fpNum = 0
        
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
            'VLP_EDP': 0,
            'FP':0,
            'LS': 0,
            'OTHER': 1
        }
