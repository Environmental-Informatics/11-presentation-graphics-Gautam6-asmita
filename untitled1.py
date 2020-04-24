#!/bin/env python
# Created on April 11, 2020
#  by Asmita Gautam
#
# This script serves as the solution set for assignment-11 on presentation
# graphics
#
#Assignment completed on: 20th april 2020
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
    
    #define column names
    #if 'filename'=='Annual_Metrics.csv':
     #   colNames = ['Date', 'site_no', 'Mean Flow' , 'Peak Flow', 'Median', 
      #              'Coeff Var','Skew','TQmean','R-B Index','7Q','3xMedian','Station']
    #else:
     #   colNames = ['Date', 'site_no', 'Mean Flow', 'Coeff Var', 'TQmean',"R-B Index","Station"]

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
    plt.legend()
    plt.title('Last 5 year daily flow ')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Last 5 year daily flow.png',dpi=96)
    plt.close()
    
    
    #Read in data
    Annual_Met = ReadMetrics(Metrics['Annual'])
    Monthly_Met =ReadMetrics(Metrics['Monthly'])
    Tipe_Annual_Met= Annual_Met[Annual_Met['Station']=='Tippe']
    # define bank dictionaries 
    Metric= {}
    for file in Metrics.keys():
        
        Metric[file] = ReadMetrics(Metrics[file])
        
        #For plotting data
        plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Wildcat']['Coeff Var'],'b')
        plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Tippe']['Coeff Var'],'r')
    plt.legend([riverName['Wildcat'],riverName['Tippe']])
    plt.title('Annual Coefficient of Variation')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Annual coeff var.png',dpi=96)
    plt.close()
        
    #plt.close()
          
        #For plotting data
    plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Wildcat']['TQmean'],'b')
    plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Tippe']['TQmean'],'r')
    plt.legend([riverName['Wildcat'],riverName['Tippe']])
    plt.title('Annual TQmean')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Year')
    plt.tight_layout()
    plt.rcParams.update({'font.size':12})
        
    #Save plot
    plt.savefig('Annual TQmean.png',dpi=96)
    plt.close()
    
    #
    plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Wildcat']['R-B Index'],'b')
    plt.plot(Metric['Annual'].loc[Metric['Annual']['Station']=='Tippe']['R-B Index'],'r')
    plt.legend([riverName['Wildcat'],riverName['Tippe']])
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
    
    for name,data in MonthlyDF:
        columns=['Mean Flow']
        m=[3,4,5,6,7,8,9,10,11,0,1,2]
        index=0
        
        avdata=pd.DataFrame(0,index=range(1,13),columns=columns)
        
        for i in range (1,13):
            avdata.iloc[index,0]= data['Mean Flow'][m[index]::12].mean()
            index+=1
            
        plt.plot(avdata.index.values,avdata['Mean Flow'].values,label=riverName[name])
    plt.legend()
    plt.title('Average annual monthly flow')
    plt.ylabel('Discharge (cfs)')
    plt.xlabel('Month')
    plt.tight_layout()
    plt.rcParams.update({'font.size':20})
        
    #Save plot
    plt.savefig('Monthly_flow.png',dpi=96)
    plt.close()
        #plt.close()
    
    #Import annual data
    AnnualMetric = ReadMetrics(Metrics['Annual'])
    AnnualDF=AnnualMetric.drop(columns=['site_no', 'Mean Flow', 'Median',
                                        'Coeff Var','Skew','TQmean','R-B Index','7Q','3xMedian'])
    AnnualDF=AnnualDF.groupby('Station')
    
    #
    
    pflow=AnnualMetric.sort_values('Peak Flow', ascending=False)
    rank1=stats.rankdata(pflow['Peak Flow'], method='average')
    rank2=rank1[::-1]
    ep=[(rank2[i]/(len(pflow)+1)) for i in range(len(pflow))]
        
        #
    plt.scatter(ep,pflow['Peak Flow'],label=riverName[name])
        
    plt.legend()
    plt.title('Period of Annual Peak flow')
    plt.xlabel('Exceedence Probability(%)')
    plt.ylabel('Peak Discharge(cfs) ')
    plt.tight_layout()
    plt.rcParams.update({'font.size':20})
        
    #Save plot
    plt.savefig('Exceed_Prob.png',dpi=96)
    plt.close()
        
    