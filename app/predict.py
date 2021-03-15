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
    unEmp90: int = Field(..., example=1)
    foodWrkr: int = Field(..., example=1)


@router.post('/predict')
async def determine_eligibility(zipcode, family_size, income, unEmp90, foodWrkr, minorGuest):

    
    income_goal = income_filter[int(family_size)]

    try:
        
        user_income = int(income) * 12

        for z in zips_filter:
            
            if int(z) == int(zipcode):

                if unEmp90 == '1':

                    if int(user_income) <= income_goal:
                        
                        return {
                            'SNAP': 1,
                            'CC': 0,
                            'FP': 0
                            }

                    else:
                        return {
                            'SNAP' : 0,
                            'CC' : 0,
                            'FP' : 1
                        }

            
                else:
                    return {
                        'SNAP': 0,
                        'CC': 0,
                        'FP': 1
                    }
        return {
            'SNAP':0,
            'CC':0,
            'FP':0
            }
                
    except:

        return {
                    'SNAP':0,
                    'CC':0,
                    'FP':0
                }
