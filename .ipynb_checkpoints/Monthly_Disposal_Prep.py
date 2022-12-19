
import pandas as pd


#Wirting the ages on serperate sheet
with pd.ExcelWriter("age.xlsx") as writer:
        memodf.to_excel(writer)

from abc import  ABC, abstractmethod
from datetime import datetime
import re


class handlerInterface (ABC):

    
    name = "handlerInterface"
    output = pd.DataFrame()

    @abstractmethod
    def cleanUp(): 
        pass

    @classmethod
    def printer(cls):
        link = "output/" + cls.name + ".xlsx"
        with pd.ExcelWriter(link) as writer:
            cls.output.to_excel(writer)
        
        

#Define indiviudal processing to the input
class AgeInterface(handlerInterface):

    name = "Age"
    
    @classmethod
    def cleanUp(cls, dataframe):
        try: 
            reqDetails = dataframe['Memo']
            cls.output = pd.DataFrame(reqDetails.str.extract(r'([\w]?[\w](?=(\s+)?[yY](ea)?rs?))'))
            cls.output.isna = "No Age"
            cls.output = cls.output.fillna("")
            return cls.output
        except KeyError as key:
            print('Key Not Found in Age Interface', key)
"""
Spend Categories in the report
     -HVAC
     -Exterior Structure
     -Plumbing
     -Amenity Spaces
     -Parking & Outdoor Storage
     -Fire alarm/Sprinkler
     -Electrical Systems
"""
class WTInterface(handlerInterface):

    name = "Welltower_OB"

    @classmethod
    def cleanUp(cls, dataframe):
        try:
            marOBregex = re.compile("[Oo]pening|PPA(?!(\s\w+)?(\s|)?adjust)")
            MarOBfilter = dataframe["Asset ID"].str.contains( marOBregex ,regex=True)
            cls.output = dataframe[MarOBfilter]
            cls.output = cls.output.pivot_table(index = ["Worktags", "Spend Category", "Asset ID", "Asset Status"])
            return cls.output
        except KeyError as key:
            print('Key Not Found in WTInterface', key)

"""
To instaniated

"""
class Outputs(AgeInterface, WTInterface):
        
        def __init__(self, dataframe ):
            #taking into account mutlity inheritance
            self.ageDataframe  = AgeInterface.cleanUp(dataframe)
            self.WTDataframe  = WTInterface.cleanUp(dataframe)
            

        def agePrinter(self):
            AgeInterface.printer()

        def WTPritner(self):
            WTInterface.printer()

#Idea is for this to work as a interface for other class to so it can take the functionailty of the dataframes
#converts RFJL, Asset and Req xlsx to Dataframes 
class Inputs(): 

        monthDigit = datetime.now().month
        monthStr = datetime.now().strftime("%b")

        def __init__(self):
                self._dataframe = pd.DataFrame()
               
       #@abstractmethod
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
                  self._dataframe = pd.read_excel(link, sheet_name=f"{Inputs.monthStr} 2022", header= 5) if type == "AGE"  else pd.read_excel(f"{file}.xlsx")
                        
                









    

    



