
import pandas as pd




from abc import  ABC, abstractmethod
from datetime import datetime
import re

#Generic Interface
class handlerInterface (ABC):

    
    name = "handlerInterface"
    output = pd.DataFrame()

    #Data Cleansing & Manpulation
    @abstractmethod
    def cleanUp(): 
        pass
    
    #Generic Panda Excel outstream
    @classmethod
    def printer(cls):
        link = "output/" + cls.name + ".xlsx"
        with pd.ExcelWriter(link) as writer:
            cls.output.to_excel(writer)
        
        

#Provides Class methods that cleanse data and extract the age number
class AgeInterface(handlerInterface):

    name = "Age"
    

    #Note that this method utilizes the class variable output to for it's dataframe 
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
#Provides Class methods that cleanse data to for Wellt
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
To instaniated and implemented
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

"""
Classifies xl files and converts them to objects that 
can later be pass though to Output 
and then be modified thorugh the interface extension.
"""
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
                  #destructing a tuple
                  type, file = kind
                except:
                  raise ValueError("Pass an iterable with two items")
                else:
                  link =  Inputs.monthStr +"2022.xlsx"
                  self._dataframe = (pd.read_excel(link, sheet_name=f"{Inputs.monthStr} 2022", header= 5) 
                                    if type == "AGE"  
                                    else pd.read_excel(f"{file}.xlsx"))


                        
"""

        The req sheet will be the month and year eg.
                         "Dec2022"

The WT asset sheet will be user defined following this naming convention EG.
             'WelltowerAssetData_(month&day)*nospaces*'

"""
def main():


    reqdf = Inputs()
    #set the in inflow stream  - tuple 
    reqdf.dataframe = ('AGE', '')
    age = Outputs(reqdf.dataframe)
    age.output
    age.agePrinter()

    # wtdf = Inputs()
    # #set the in inflow stream - tuple, 2nd
    # wtdf.dataframe =('NOT AGE', 'WelltowerAssetData_1216')
    # wtOB = Outputs(wtdf.dataframe)
    # test = wtOB.WTDataframe
    # wtOB.output
    # wtOB.WTPritner()









    

    



