import streamlit as sl
import requests
import pandas as pd
import json

url = "http://192.168.2.68:5000/"

def fetch_data(path):
    data = requests.get(url+path)
    return json.loads(data.text)['price']

sl.set_page_config(page_title="Energy Prices",layout="wide")
sl.header("""Energy""")
left, right = sl.columns(2)

now = fetch_data('now')
left.metric("Now", str(now) + " €/Kwh")


def percentage_dif(now, n):
    return str(round((n-now)/now*100,2))

data = fetch_data('next')
n1 = data[0][1]
n2 = data[1][1]
n3 = data[2][1]
col1, col2, col3 = left.columns(3) 
col1.metric(data[0][0], str(n1) + " €/Kwh", percentage_dif(now, n1) + "%", delta_color="inverse")
col2.metric(data[1][0], str(n2) + " €/Kwh", percentage_dif(now, n2) + "%", delta_color="inverse")
col3.metric(data[2][0], str(n3) + " €/Kwh", percentage_dif(now, n3) + "%", delta_color="inverse")

data = fetch_data('today')
today = []
for ele in data:
    today.append([int(ele[0]),float(ele[1])])
today = pd.DataFrame(today, columns=['hours','energy prices'])
left.write("""### Today""")
graph = left.empty()
graph.line_chart(data = today, x= 'hours', y = 'energy prices')

data = fetch_data('tomorrow')
tomorrow = []
for ele in data:
    tomorrow.append([int(ele[0]),float(ele[1])])
tomorrow = pd.DataFrame(tomorrow, columns=['hours','energy prices'])
right.write("""### Tomorrow""")
graph = right.empty()
graph.line_chart(data = tomorrow, x= 'hours', y = 'energy prices')

data = fetch_data('all')
all = []
for ele in data:
    all.append([int(ele[0]),float(ele[1])])

all = pd.DataFrame(all, columns=['hours','energy prices'])

right.write("""### All""")
graph = right.empty()
graph.line_chart(data = all, x= 'hours', y = 'energy prices')