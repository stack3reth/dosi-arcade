import requests
import pandas as pd
from datetime import datetime

####################################################################
def fetch_data(url, headers=None, timestamp=None):
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Error:", response.status_code)
        return None

def format_number(value):
    if pd.notnull(value) and isinstance(value, (int, float)):
        return '{:,.0f}'.format(value)
    return value

def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer pT1euenXWTM7xS5Os2EqhnumXmYwtF1tpJHivQKGdzr'}
    payload = {'message': message}
    r = requests.post(url, headers=headers, data=payload)
    return message

####################################################################
def main():
    url_rainbow = "https://citizen.dosi.world/api/citizen/v1/arcade/rainbowblast/ranking"
    url_penguin = "https://citizen.dosi.world/api/citizen/v1/arcade/penguindash/ranking"
    url_hexa = "https://citizen.dosi.world/api/citizen/v1/arcade/hexacube/ranking"

    result = fetch_data(url_rainbow).get('rankList')
    selected_columns = ['rank', 'displayName', 'score']
    rainbow = [{col: row[col] for col in selected_columns} for row in result]
    rainbow = pd.DataFrame(rainbow)

    result = fetch_data(url_penguin).get('rankList')
    selected_columns = ['rank', 'displayName', 'score']
    penguin = [{col: row[col] for col in selected_columns} for row in result]
    penguin = pd.DataFrame(penguin)

    result = fetch_data(url_hexa).get('rankList')
    selected_columns = ['rank', 'displayName', 'score']
    hexa = [{col: row[col] for col in selected_columns} for row in result]
    hexa = pd.DataFrame(hexa)

    message = "Top 10 Arcade Snapshot\n 🕖"+ datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " (UTC+7)"

    message = message+"\n\n🌈 Rainbow Blast\n"
    for i, r in rainbow.iterrows():
        m = str(r['rank'])+" "+r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
    
    message = message+"\n🐧 Penguin Dash\n"
    for i, r in penguin.iterrows():
        m = str(r['rank'])+" "+r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
        
    message = message+"\n💎 Hexa Cube\n"
    for i, r in hexa.iterrows():
        m = str(r['rank'])+" "+r['displayName']+" ("+str(format_number(r['score']))+")\n"
        message = message+m
        
    print(line_notify(message))

####################################################################
if __name__ == "__main__":
    main()