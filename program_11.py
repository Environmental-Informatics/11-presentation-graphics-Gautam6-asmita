#!/bin/env python
# Created on April 11, 2020
#  by Asmita Gautam
#
# This script serves as the solution set for assignment-11 on presentation
# graphics
#
#Assignment completed on: 24th april 2020
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "agency_cd", "site_no", "Date", "Discharge", "Quality". The 
    "Date" column should be used as the DataFrame index. The pandas read_csv
    function will automatically replace missing values with np.NaN, but needs
    help identifying other flags used by the USGS to indicate no data is 
    availabiel.  Function returns the completed DataFrame, and a dictionary 
    designed to contain all missing value counts that is initialized with
    days missing between the first and last date of the file."""
    
    #define column names
    colNames = ['agency_cd', 'site_no', 'Date', 'Discharge', 'Quality']

    # open and read the file
    DataDF = pd.read_csv(fileName, header=1, names=colNames,  
                         delimiter=r"\s+",parse_dates=[2], comment='#',
                         na_values=['Eqp'])
    DataDF = DataDF.set_index('Date')
    
    #Negative discharge values to NaN
    DataDF.loc[~(DataDF['Discharge']>0),'Discharge']=np.nan
    # quantify the number of missing values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )

def ClipData( DataDF, startDate, endDate ):
    """This function clips the given time series dataframe to a given range 
    of dates. Function returns the clipped dataframe and and the number of 
    missing values."""
    #For cliping data
    DataDF=DataDF[startDate:endDate]
    
    #Counting nodata values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )

def ReadMetrics( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    the metrics from the assignment on descriptive statistics and 
    environmental metrics.  Works for both annual and monthly metrics. 
    Date column should be used as the index for the new dataframe.  Function 
    returns the completed DataFrame."""
    
   
    # open and read the file
    DataDF = pd.read_csv(fileName, header=0,delimiter=",",
                         parse_dates=['Date'], comment='#',
                         )
    DataDF=DataDF.set_index('Date')
    
    return( DataDF )


# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    # define full river names as a dictionary so that abbreviations are not used in figures
    riverName = { "Wildcat": "Wildcat Creek",
                  "Tippe": "Tippecanoe River" }
    
    # define filenames as a dictionary
    fileName = { "Wildcat": "WildcatCreek_Discharge_03335000_19540601-20200315.txt",
                 "Tippe": "TippecanoeRiver_Discharge_03331500_19431001-20200315.txt" }
    
    Metrics={"Annual": "Annual_Metrics.csv",
             "Monthly": "Monthly_Metrics.csv"}
    
    # define blank dictionaries (these will use the same keys as fileName)
    DataDF = {}
    MissingValues = {}
   
    # process input datasets
    for file in fileName.keys():
        
        DataDF[file], MissingValues[file] = ReadData(fileName[file])
        
        # clip to consistent period
        
        DataDF[file], MissingValues[file] = ClipData( DataDF[file], '2014-10-01', '2019-09-30' )
        
        #For plotting data
        plt.plot(DataDF[file]['Discharge'],label=riverName[file])
    plt.legend(loc='upper right')
    plt.title('Last 5 year daily flow ')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Last 5 year daily flow.png',dpi=96)
    plt.close()
    
    
    #Read in data/Metrics
    Annual_Met = ReadMetrics(Metrics['Annual'])
    Monthly_Met =ReadMetrics(Metrics['Monthly'])
    Tipe_Annual_Met= Annual_Met[Annual_Met['Station']=='Tippe']
    Wild_Annual_Met= Annual_Met[Annual_Met['Station']=='Wildcat']

        
    #For plotting data Annual Coeff Var
    plt.plot(Tipe_Annual_Met['Coeff Var'])
    plt.plot(Wild_Annual_Met['Coeff Var'])
    plt.legend([riverName['Tippe'],riverName['Wildcat']],loc='upper right')
    plt.title('Annual Coefficient of Variation')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Annual coeff var.png',dpi=96)
    plt.close()
        
          
    #For plotting data
    plt.plot(Tipe_Annual_Met['TQmean'])
    plt.plot(Wild_Annual_Met['TQmean'])
    plt.legend([riverName['Tippe'],riverName['Wildcat']],loc='upper right')
    plt.title('Annual TQmean')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Annual TQmean.png',dpi=96)
    plt.close()
    
    #Annual R-B Index
    plt.plot(Tipe_Annual_Met['R-B Index'])
    plt.plot(Wild_Annual_Met['R-B Index'])
    plt.legend([riverName['Tippe'],riverName['Wildcat']],loc='upper right')
    plt.title('Annual R-B Index ')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Annual R-B Index.png',dpi=96)
    plt.close()
        
    #import monthly data
    MonthlyMetric = ReadMetrics(Metrics['Monthly'])
    MonthlyDF=MonthlyMetric.groupby('Station')
    
    for name,data in MonthlyDF:           #As similar in Assign 10
        columns=['Mean Flow']
        m=[3,4,5,6,7,8,9,10,11,0,1,2]
        index=0
        
        avdata=pd.DataFrame(0,index=range(1,13),columns=columns)
        
        for i in range (1,13):
            avdata.iloc[index,0]= data['Mean Flow'][m[index]::12].mean()
            index+=1
            
        plt.plot(avdata.index.values,avdata['Mean Flow'].values,label=riverName[name])
    plt.legend(loc='upper right')
    #plt.xlim(0,12,2)
    plt.title('Average annual monthly flow')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Month')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Monthly_flow.png',dpi=96)
    plt.close()
    
    #Exceedance probability
    Tipe_AnnualDF= Tipe_Annual_Met.drop(columns=['site_no', 'Mean Flow', 'Median',
                                        'Coeff Var','Skew','TQmean','R-B Index','7Q','3xMedian'])
    
    Wild_AnnualDF= Wild_Annual_Met.drop(columns=['site_no', 'Mean Flow', 'Median',
                                        'Coeff Var','Skew','TQmean','R-B Index','7Q','3xMedian'])
    
    
    #Exceedance probability for Tippe river
    pflow=Tipe_AnnualDF.sort_values('Peak Flow', ascending=False)
    rank1=stats.rankdata(pflow['Peak Flow'], method='average')
    rank2=rank1[::-1]
    ep1=[(rank2[i]/(len(pflow)+1)) for i in range(len(pflow))]
    
    #
    plt.scatter(ep1,pflow['Peak Flow'],label=riverName['Tippe'])
    
    #Excedance probability for WildCat river
    pflow2=Wild_AnnualDF.sort_values('Peak Flow', ascending=False)
    rank12=stats.rankdata(pflow2['Peak Flow'], method='average')
    rank22=rank1[::-1]
    ep2=[(rank22[i]/(len(pflow)+1)) for i in range(len(pflow2))]
    
    #
    plt.scatter(ep2,pflow2['Peak Flow'],label=riverName['Wildcat'])
    plt.xlim(1,0)
    plt.ylim(0,25000,5000)
    plt.legend(loc='upper right')
    plt.title('Period of Annual Peak flow')
    plt.xlabel('Exceedence Probability')
    plt.ylabel('Peak Discharge(cfs) ')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
    
    #Save plot
    plt.savefig('Exceed_Prob.png',dpi=96)
    plt.close()
        
    