from simple_salesforce import Salesforce, SalesforceLogin
from datetime import datetime
import pandas as pd
import os

#initialize authentication settings
username=os.environ['SALESFORCE_USERNAME']
password=os.environ['SALESFORCE_PASSWORD']
token=os.environ['SALESFORCE_API_KEY']
instance='https://na153.lightning.force.com'

#instantiate query object
sf = Salesforce(username=username, password=password, security_token=token, instance_url=instance)

#Define query
convertedDateQuery = 'SELECT ConvertedDate FROM Lead'

#Create SOQL engine
def SOQL(sql_request):
    result = sf.query(sql_request)
    print(f'Total Records: {result["totalSize"]}')
    isDone = result['done']

    if isDone == True:
        df = pd.DataFrame(result['records'])

    while isDone == False:
        try:
            if result['done'] == False:
                df = df.append(pd.DataFrame(result['records']))
                result = sf.query_more(result['nextRecordsURL'], True)
            else:
                df = df.append(pd.DataFrame(result['records']))
                isDone = True
                print('completed')
                break
        except NameError:
            df = pd.DataFrame(result['records'])
            qry = sf.query_more(result['nextRecordsURL'], True)

    return df

#run query
df = SOQL(convertedDateQuery)

#clean file
df = df.dropna().drop('attributes', axis=1)
df.loc[:, 'ConvertedDate'] = pd.to_datetime(df['ConvertedDate'])
df = df.sort_values('ConvertedDate')

#message for error logs
print(df['ConvertedDate'].tail())

#save file to csv
timestamp = datetime.now().strftime('%Y-%m-%d')
filepath = 'data/Lead_'+timestamp
df.to_csv(filepath +'.csv', index=False)

