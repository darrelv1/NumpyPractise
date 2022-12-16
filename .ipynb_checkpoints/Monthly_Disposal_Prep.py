
import pandas as pd

#Requistion import
reqdets = pd.read_excel("WorkdayReqDetail_Darre.xlsx", sheet_name= "Nov 2022", header= 5)

memo = reqdets["Memo"]

reqdets.columns

import re

#age Regex utilizing lookahead assertions, x(?=y)
memodf= pd.DataFrame(memo.str.extract(r'([\w]?[\w](?=(\s+)?[yY](ea)?rs?))'))

pd.set_option('display.max_rows', memo.shape[0]+1)

memodf.isna = "No Age"

memodf =memodf.fillna("")

#Wirting the ages on serperate sheet
with pd.ExcelWriter("age.xlsx") as writer:
        memodf.to_excel(writer)

from abc import  ABC, abstractmethod
from datetime import datetime


class handlerInterface (ABC):


    @abstractmethod
    def cleanUp(): 
        pass

    @abstractmethod
    def printer():
        pass 

#Idea is for this to work as a interface for other class to so it can take the functionailty of the dataframes
#converts RFJL, Asset and Req xlsx to Dataframes 
class Inputs(ABC, handlerInterface): 

        monthDigit = datetime.now().month
        monthStr = datetime.now().strftime("%b")

        def __init__(self):
                self._dataframe = pd.DataFrame()


       # @abstractmethod
        @property
        def dataframe(self):
                return self._dataframe

        @dataframe.setter
        def dataframe(self, kind):
                #Kind will take in a tuple
                try: 
                  type, file = kind
                except:
                  raise ValueError("Pass an iterable with two items")
                else:
                  link =  Inputs.monthStr +"2022.xlsx"
                  self._dataframe = pd.read_excel(link, sheet_name=f"{Inputs.monthStr} 2022", header= 5) if type == "AGE"  else pd.read_excel(f"{file}.xlsx", sheet_name="Find Assets")
                        
                


age = Inputs()
age.dataframe = ("AGE","")
marAsset = Inputs()
marALLAsset.dataframe ("", "MAR_ALL")






    

    



