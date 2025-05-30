import pandas as pd 
import os
import subprocess
import warnings
import shutil


def log_filter(PATH):
    
    warnings.filterwarnings('ignore')

    values = os.listdir(PATH+"/")

    df=pd.DataFrame()
    merged_dataframe=pd.DataFrame()
    temp=values.pop()

    df=pd.read_csv(PATH+"/"+temp, sep='\t', header=None,skiprows=6)
    df.iloc[0]=df.iloc[0].shift(-1)
    df.iloc[1]=df.iloc[1].shift(-1)
    header=df.iloc[0].to_list()
    df=df.drop(0,axis=0)
    df.columns=header
    df=df.drop_duplicates('uid', keep='last')

    for log_file in values:
        print(log_file)
        df1=pd.read_csv(PATH+"/"+log_file, sep='\t', header=None,skiprows=6)
        df1.iloc[0]=df1.iloc[0].shift(-1)
        df1.iloc[1]=df1.iloc[1].shift(-1)
        header=df1.iloc[0].to_list()
        df1=df1.drop(0,axis=0)
        df1.columns=header
        df1=df1.drop_duplicates('uid', keep='last')
        columns_to_use=df1.columns.difference(df.columns)
        df=pd.merge(df, df1[columns_to_use],left_index=True, right_index=True, how='left')
    
    return df

def zeek_process(file_name):

    path="/home/omrapp/Desktop/reporthash/returned_network_logs/trafficLogs/"
    PATH="/home/omrapp/Desktop/reporthash/returned_network_logs/trafficLogs/eno1_"+file_name+".pcap"
    logsdir='/home/omrapp/Desktop/reporthash/returned_network_logs/trafficLogs/logs'

    os.system(f'rm -rf {logsdir}')
    os.system(f'mkdir {logsdir}')


    # p0=subprocess.Popen(["pcapfix",PATH,"-o",PATH])
    # p0.wait()
    
    print("Starting zeek processing")
    p0=subprocess.Popen([f"/usr/local/zeek/bin/zeek -r /home/omrapp/Desktop/reporthash/returned_network_logs/trafficLogs/eno1_{file_name}.pcap"], shell=True)
    p0.wait()

    print("Finishing zeek processing")

    values=["analyzer.log",
            "conn.log",
            "dns.log",
            "dpd.log",
            "files.log",
            "http.log",
            "kerberos.log",
            "ldap.log",
            "modbus.log",
            "ntp.log",
            "packet_filter.log",
            "ssh.log",
            "ssl.log",
            "weird.log",
            "x509.log"]
    
    values = list(set(values) - set(["kerberos.log",'packet_filter.log', 'x509.log'])) #files commented as they do not have a UID's column 
   

    for log in values:
            print(log)
            try:
                ft=os.system('mv '+log+" ~/Desktop/reporthash/returned_network_logs/trafficLogs/logs"+" > /dev/null 2>&1" )
                if ft>0:
                    raise "File not found"
                else:
                    print("OK")
                # shutil.copy2(log,"~/Desktop/reporthash/returned_network_logs/trafficLogs/logs")
            except:
                print("File not present, It may have already be transfered, or may be forbidden")
                continue

    print("Finished log file transfer to the logs directory\n")
    print("Removing non-used logs")
    os.system('rm *.log')
    print("Removed logs")

    
    print("Now filtering the logs")

    processed_df=log_filter(logsdir)
    processed_df.to_csv("/home/omrapp/Desktop/reporthash/radar_processed_networktrails_"+file_name+".csv")
    

#Below code for running tests only 
# value=input("Enter filename ")
# zeek_process(value)