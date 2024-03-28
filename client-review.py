import streamlit as st
import plotly.express as px #pip install plotly_express 
import pandas as pd  #pip install pandas
import os
import warnings
warnings.filterwarnings('ignore')

## All Demos to be in Wide Layout
#st.set_page_config(layout="wide")
st.set_page_config(page_title="Advisor's Client Nexus", page_icon='favicon.ico',  layout="wide")
#st.set_page_config(page_title='Famiology.docdetector', page_icon='/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')

#This is Famiology Branding Banner
st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)


st.title("Client & Prospect Review")
st.subheader("Are we targeting right professional communities?")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.sidebar.header("About App")
#st.sidebar.subheader("Advisor's Client Nexus")

with st.sidebar.expander("Advisor's Client Nexus",True):

    st.write(

    """

        Welcome to the Wealth Advisor's Client Nexus, designed to provide an overview of your client base and potential prospects.

        Targeting the right professional communities is essential for the success!!

    """

)
st.sidebar.divider()

df = pd.read_excel(io='FamilyOfficeEntityDataSampleV1.1.xlsx',
                engine='openpyxl',
                       sheet_name='Client Profile' )
    
    #print(df)

col1, col2 = st.columns((2))
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"])
startDate = pd.to_datetime(df["Date of Birth"]).min()
endDate = pd.to_datetime(df["Date of Birth"]).max()

with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
      
with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date of Birth"] >= date1) & (df["Date of Birth"] <= date2)]
df2 = df[(df["Date of Birth"] >= date1) & (df["Date of Birth"] <= date2)]
df3 = df[(df["Date of Birth"] >= date1) & (df["Date of Birth"] <= date2)]
df4 = df[(df["Date of Birth"] >= date1) & (df["Date of Birth"] <= date2)]
st.sidebar.header("Choose your filter: ")

#create for Status
status = st.sidebar.multiselect("Pick the Client Status", df["Status"].unique())
if not status:
       df2 = df.copy()
else:
      df2 = df[df["Status"].isin(status)]

state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not status:
       df3 = df2.copy()
else:
      df3 = df2[df2["State"].isin(state)]

profession = st.sidebar.multiselect("Pick the Community", df3["Profession"].unique())
if not profession:
       df4 = df3.copy()
else:
      df4 = df3[df3["Profession"].isin(profession)]

if not status and not state and not profession:
       filtered_df = df
elif  not state and not profession:
       filtered_df = df[df["Status"].isin(status)]
elif not status and not profession:
       filtered_df = df[df["State"].isin(state)]
elif state and profession:
       filtered_df = df4[df4["State"].isin(state) & df4["Profession"].isin(profession)]
elif status and profession:
       filtered_df = df4[df4["Status"].isin(status) & df4["Profession"].isin(profession)]
elif status and state:
       filtered_df = df3[df3["Status"].isin(status) & df3["State"].isin(state)]
elif profession:
      filtered_df = df4[df4["Profession"].isin(profession)]

status_df =  filtered_df.groupby(by = ["Status","State"], as_index = False)["Net Worth"].sum()

with col1:
       st.subheader("Status & State wise Net Worth review")
       fig = px.bar(status_df, x = "Status", y = 'Net Worth', text='State',
                    template="seaborn")
       
       st.plotly_chart(fig, use_container_width=True, height = 200)

profession_df =  filtered_df.groupby(by = ["Profession","State"], as_index = False)["Net Worth"].sum()
with col2:
       st.subheader("Community wise Net Worth review")
       fig = px.pie(profession_df, values = "Net Worth", names = "Profession", hole=0.5, hover_data="State") 
       fig.update_traces(text = profession_df["Profession"], textposition = "outside")  
       st.plotly_chart(fig, use_container_width=True) 