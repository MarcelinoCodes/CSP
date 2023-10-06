"""
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
"""

# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import numpy as np


# Incorporate data
df = pd.read_csv('dataset.csv')
df=df.drop_duplicates()
#df=df.dropna()
df=df.drop(columns=[df.columns[5]])

# Make a bar chart that displays how many times each brand of car appears in this data. 
freq={}
for i in df["WHOIS_COUNTRY"]:
    if i not in freq:
        freq[i]=1
    else:
        freq[i]+=1
       
#Make the horizontal barchart (for countries)
keys = list(freq.keys())
values = list(freq.values())
sorted_value_index = np.argsort(values)
sorted_dict = {keys[i]: values[i] for i in sorted_value_index} # I visualized the data, everyother value is fodder

#visualie those with values greater than 5
real_sorted_dict={}
for i in sorted_dict:
  if sorted_dict[i]>5 and i!='None':
    real_sorted_dict[i]=sorted_dict[i]

x_lab=list(real_sorted_dict.values())
y_lab=list(real_sorted_dict.keys())

data=[]
for i in range(len(x_lab)):
    data.append([x_lab[i],y_lab[i]])

df = pd.DataFrame(data, columns=['LINKS', 'COUNTRY'])


#2nd plot (Making the graph showing the percentage of the )
df_phish=pd.read_csv('malicious_phish.csv')
df_malignant=df_phish[df_phish['type']!='benign']
df_malignant=df_malignant.reset_index()
list_of_extensions=['.nl','.be','.hu','.it','.ir','.pl','.de','.br','.ac']
times_extensions_appear={'.nl':0,'.be':0,'.hu':0,'.it':0,'.ir':0,'.pl':0,'.de':0,'.br':0,'.ac':0}

for i in range(len(df_malignant['url'])):
    for j in range(len(list_of_extensions)):
        word=list_of_extensions[j]
        if word in df_malignant['url'][i] and 'www.'+word not in df_malignant['url'][i]:
            times_extensions_appear[word]+=1

keys = list(times_extensions_appear.keys())
values = list(times_extensions_appear.values())
sorted_value_index = np.argsort(values)
sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
sorted_dict

x_lab=list(sorted_dict.values())
for i in range(len(x_lab)):
    x_lab[i]/=len(df_malignant)
y_lab=list(sorted_dict.keys())

data=[]
for i in range(len(x_lab)):
    data.append([x_lab[i],y_lab[i]])

dff = pd.DataFrame(data, columns=['NUMBER', 'EXTENSIONS'])


#plot 3 (plotting by types of attacks)
df_phish=pd.read_csv('malicious_phish.csv')
phishing=0
defacement=0
malware=0

for i in df_phish['type']:
    if i=='phishing':
        phishing+=1
    elif i=='defacement':
        defacement+=1
    elif i=='malware':
        malware+=1
all_malicious=(phishing+defacement+malware)/len(df_phish['type'])
#(phishing+defacement+malware)/len(df_phish['type']) Over a 3rd of all websites are malicious
L=len(df_phish['type'])
data=[['All Websites',1],['All Malicious Websites', all_malicious],['phishing',phishing/L],['defacement',defacement/L],['malware',malware/L]]
dfff=pd.DataFrame(data,columns=['category','percentage'])

# 4th graph wil show the number of malicious links by state
data=[['California',429],['New York',86],['Washington',75],['Florida',61],['Texas',19]]
dffff=pd.DataFrame(data,columns=['State','Number of Links'])
# Initialize the app
app = Dash(__name__)


#5th plot
data=[['Apache',121],['nginx',66],['Microsoft',16]]
dfffff=pd.DataFrame(data,columns=['Server','Number of Malicious Links'])
#6th plot



# App layout
app.layout = html.Div([
    html.H1("Ploting the relationship of malicious urls and their recurrence by States and Countries"),
    dcc.Graph(figure=px.histogram(df, x='COUNTRY', y='LINKS', histfunc='sum'),style={'display': 'inline-block'}),
    dcc.Graph(figure=px.histogram(dff, x='NUMBER', y='EXTENSIONS', histfunc='sum'),style={'display': 'inline-block'}),
    dcc.Graph(figure=px.histogram(dfff, x='category', y='percentage', histfunc='sum'),style={'display': 'inline-block'}),
    dcc.Graph(figure=px.histogram(dffff, x='State', y='Number of Links', histfunc='sum'),style={'display': 'inline-block'}),
    dcc.Graph(figure=px.histogram(dfffff, x='Server', y='Number of Malicious Links', histfunc='sum'),style={'display': 'inline-block'})
])

# Run the apps
if __name__ == '__main__':
    app.run(debug=True)
