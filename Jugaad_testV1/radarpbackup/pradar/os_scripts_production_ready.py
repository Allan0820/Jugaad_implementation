import pandas as pd

def os_scripts(filename):
   
   path="/home/omrapp/Desktop/reporthash/"
   PATH="/home/omrapp/Desktop/reporthash/returned_os_logs/"+filename
#    logsdir='/home/omrapp/Desktop/reporthash/trafficLogs/logs'
   
   df=pd.read_pickle("/home/omrapp/Desktop/Jugaad_testV1/base_image.pkl")
   df1=pd.read_csv(PATH)
   
   '''For the first dataframe'''

   keys=df['Process Name'].unique()
   dict={key: [] for key in keys } # using dictionary comprehension
   
   for i in range(0,len(df['Process Name'])):
        process=df['Process Name'].iloc[i]
        process_id=df['PID'].iloc[i]
        if process_id not in dict[process]:
            dict[process].append(process_id)

   '''For the second dataframe'''
   
   keys=df1['Process Name'].unique()
   dict1={key: [] for key in keys } # using dictionary comprehension

   for i in range(0,len(df1['Process Name'])):
        process=df1['Process Name'].iloc[i]
        process_id=df1['PID'].iloc[i]
        if process_id not in dict1[process]:
            dict1[process].append(process_id)

   processes_to_exclude=list(set(df['Process Name'])-set(dict1.keys()).symmetric_difference(set(dict.keys())))
    
   for x in processes_to_exclude:
            i=(df[(df['Process Name']==x)].index)
            df.drop(index=list(i), inplace=True)
   df.to_csv("os_filtered", sep=",")
   df.index = range(1, len(df) + 1)
   df.to_csv(path+"radar_processed_ostrails_"+filename+".csv")


# filename=input("Please give csv file name ")
# os_scripts(filename)

