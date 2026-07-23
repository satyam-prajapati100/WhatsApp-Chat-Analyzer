import re 
import pandas as pd 

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s)'

    messages= re.split(pattern ,data)[2::2] 
    dates= re.split(pattern ,data)[1::2]

    df = pd.DataFrame({
    'user_message': messages,
    'message_date': dates
    })
    # clean extra "-"
    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=False)
    # Convert string to datetime
    
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %I:%M %p'
    )
    
    
    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    msgs = []
    
    for message in df['user_message']:
    
        match = re.match(r'^([^:]+):\s(.*)$', message)
    
        if match:
            users.append(match.group(1))
            msgs.append(match.group(2))
        else:
            users.append('group_notification')
            msgs.append(message)
    
    df['user'] = users
    df['message'] = msgs 
    df.drop(columns=['user_message'] , inplace=True) 

    df['only_date']=df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num']= df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period=[]

    for hour in df[['day_name','hour',]]['hour']:
        if hour == 23:
            period.append(str(hour)+ "-" + str('00'))

        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else :
            period.append(str(hour) + "-" + str(hour+1))   

    df['period']=period             


    return df
    

