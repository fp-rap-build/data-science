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

income_filter = {1:43350, 2:49550, 3:55750,
                  4:61900, 5:66900, 6:71580,
                  7:76800, 8:81750}


zips_filter = [99001, 99001, 99001, 99001, 99001, 99001, 99001, 99001, 99003,
        99003, 99003, 99003, 99003, 99003, 99003, 99003, 99004, 99004,
        99004, 99004, 99004, 99004, 99004, 99004, 99004, 99004, 99005,
        99005, 99005, 99005, 99005, 99005, 99006, 99006, 99006, 99006,
        99006, 99006, 99006, 99006, 99009, 99009, 99009, 99009, 99009,
        99009, 99009, 99009, 99011, 99011, 99011, 99011, 99011, 99011,
        99011, 99011, 99012, 99012, 99012, 99012, 99012, 99012, 99012,
        99012, 99016, 99016, 99016, 99016, 99016, 99016, 99016, 99016,
        99018, 99018, 99018, 99018, 99018, 99018, 99018, 99018, 99019,
        99019, 99019, 99019, 99019, 99019, 99019, 99019, 99020, 99020,
        99020, 99020, 99020, 99020, 99020, 99020, 99021, 99021, 99021,
        99021, 99021, 99021, 99021, 99021, 99022, 99022, 99022, 99022,
        99022, 99022, 99022, 99022, 99023, 99023, 99023, 99023, 99023,
        99023, 99023, 99023, 99025, 99025, 99025, 99025, 99025, 99025,
        99025, 99025, 99027, 99027, 99027, 99027, 99027, 99027, 99027,
        99027, 99030, 99030, 99030, 99030, 99030, 99030, 99030, 99030,
        99031, 99031, 99031, 99031, 99031, 99031, 99031, 99031, 99036,
        99036, 99036, 99036, 99036, 99036, 99036, 99036, 99037, 99037,
        99037, 99037, 99037, 99037, 99037, 99037, 99039, 99039, 99039,
        99039, 99039, 99039, 99039, 99039, 99201, 99201, 99201, 99201,
        99201, 99201, 99201, 99201, 99202, 99202, 99202, 99202, 99202,
        99202, 99202, 99202, 99203, 99203, 99203, 99203, 99203, 99203,
        99203, 99203, 99204, 99204, 99204, 99204, 99204, 99204, 99204,
        99204, 99205, 99205, 99205, 99205, 99205, 99205, 99205, 99205,
        99206, 99206, 99206, 99206, 99206, 99206, 99206, 99206, 99207,
        99207, 99207, 99207, 99207, 99207, 99207, 99207, 99208, 99208,
        99208, 99208, 99208, 99208, 99208, 99208, 99212, 99212, 99212,
        99212, 99212, 99212, 99212, 99212, 99216, 99216, 99216, 99216,
        99216, 99216, 99216, 99216, 99217, 99217, 99217, 99217, 99217,
        99217, 99217, 99217, 99218, 99218, 99218, 99218, 99218, 99218,
        99218, 99218, 99223, 99223, 99223, 99223, 99223, 99223, 99223,
        99223, 99224, 99224, 99224, 99224, 99224, 99224, 99224, 99224,
        99016, 99016, 99016, 99016, 99016, 99016, 99016, 99016]

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    zipcode: int = Field(..., example=99205)
    family_size: int = Field(..., example= 4)
    income: int = Field(..., example= 4000)
    unEmp90: str = Field(..., example='1')
    foodWrkr: str = Field(..., example='1')
    rent: int = Field(..., example=800)
    minorGuest: str = Field(..., example='1')
    covidFH: str = Field(..., example='1')


@router.post('/predict')
async def determine_eligibility(zipcode, family_size, income, rent, unEmp90, foodWrkr, minorGuest, covidFH):
    
    income_goal = income_filter[int(family_size)]

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

                            return {
                                'SNAP:ERAP': 0,
                                'SNAP:ERA': 1,
                                'CC': 0,
                                'FP': 0
                                }
                        else:
                            pass

                    else:
                        pass

                else:

                    if int(user_income) <= income_goal:

                        if (int(rent) / int(income) ) >= .50:

                            return {
                                'SNAP:ERAP': 1,
                                'SNAP:ERA': 0,
                                'CC': 0,
                                'FP': 0
                                }
                        else:
                            pass

        if minorGuest == '1':

            return {
                'SNAP:ERAP': 0,
                'SNAP:ERA': 0,
                'CC': 0,
                'FP': 1
            }

        else:
            pass


    except:
        return 'oops'
