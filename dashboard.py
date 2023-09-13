import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime


#Page heading 
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("PROJECT DASHBOARD")
# Load the CSV data
data = pd.read_csv('data.csv')

see_fulldata = st.expander('To view data👉')
with see_fulldata:
    st.write(data.head())

#designation_filter = st.sidebar.selectbox("Select Designation", ["All"] + list(set(data["DESIGNATION"])))
#work_filter = st.sidebar.selectbox("Select Work", ["All"] + list(set(data["WORK ASSIGNED"])))


# DataFrame
df = pd.DataFrame(data)


#SECTION - PROGRESSBAR FOR PROJECT
# Define the start date, end date, and current date
start_date = datetime(2023, 9, 4)
end_date = datetime(2023, 11, 4)
current_date = datetime.now()
# Calculate the progress as a percentage
total_days = (end_date - start_date).days
progress_days = (current_date - start_date).days
progress_percentage = min(progress_days / total_days, 100)
# Display the progress bar
st.title("Project progress")
st.progress(progress_percentage)
col1, col2, col3 , col4= st.columns([1,1,1,1])
with col1:
    st.write("TOTAL DAYS :",total_days)
with col2:
    st.write("DAYS COMPLETED:",progress_days)
with col3:
    st.write("DAYS REMAINING:", total_days-progress_days)
with col4:
    st.write(f"Progress: {progress_percentage*100:.2f}%")



# SECTION - PIE CHART ON PROGRESS
# Function to split and count status values
def count_status(status_str):
    return status_str.split(',')
# Apply the count_status function to each row in the DataFrame
df['status_list'] = df['STATUS'].apply(count_status)
# Create a list of all status values
all_status = [status for sublist in df['status_list'] for status in sublist]
# Count the occurrences of each status
status_counts = pd.Series(all_status).value_counts().reset_index()
status_counts.columns = ['status', 'count']
# Create a pie chart using Plotly Express
fig = px.pie(status_counts, values='count', names='status', title='Task distribution')
# Display the pie chart in Streamlit
st.title("Status of Tasks")
st.plotly_chart(fig)



# SECTION - DEADLINE COMING SOON  
# Convert date columns to datetime objects
#df['END-DATE'] = pd.to_datetime(df['END-DATE'])
df['PLANNED FINISHH'] = pd.to_datetime(df['PLANNED FINISH'])
# Calculate the current date
current_date = datetime.now()
# Filter rows where 'PLANNED-FINISH' is within 2 days of the current date
deadline_df = df[(( df['PLANNED FINISHH'] - current_date ).dt.days <= 2) & ((df['PLANNED FINISHH'] - current_date ).dt.days > 0)]
# Display the 'deadline_df'
# st.header('Deadline soon approaching', divider='rainbow')
st.header('Deadline soon approaching', divider='rainbow')
st.write(deadline_df[['NAME','WORK ASSIGNED','TASKS ASSIGNED','PLANNED FINISH']].head())


# WORKS and DEADLINES CROSSED 

df_works = df['WORK ASSIGNED']
st.sidebar.header("Works in the project :",divider="rainbow")
st.sidebar.write(df_works)
df_crossed = df[(df['PLANNED FINISHH'] - current_date ).dt.days < 0]
st.sidebar.header('Deadlines crossed', divider='red')
st.sidebar.write(df_crossed[['NAME','WORK ASSIGNED','TASKS ASSIGNED','PLANNED FINISH']].head())


df_melted = df[['WORK ASSIGNED','PLANNED START','ACTUAL START']]

# Streamlit app
st.title("Date vs Work Assigned")

# Create a Plotly scatter plot
fig = px.scatter(
    df_melted,
    x="WORK ASSIGNED",
    y=pd.to_datetime(df_melted['PLANNED START']).dt.date, # Extract dates from the "Date" column
    title="Date vs Work Assigned",
)
# Add labels to the axes
fig.update_xaxes(title_text="Work Assigned")
fig.update_yaxes(title_text="Date")
fig1 = px.scatter(
    df_melted,
    x="WORK ASSIGNED",
    y=pd.to_datetime(df_melted['ACTUAL START']).dt.date,
    title="Date vs Work Assigned",
)
fig1.update_xaxes(title_text="Work Assigned")
fig1.update_yaxes(title_text="Date")

col1, col2= st.columns([1,1])
with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig)
# Display the figure in Streamlit

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# # Reshape the DataFrame to have dates in separate columns
# df["PLANNED START"] = pd.to_datetime(df["PLANNED START"], format="%Y-%m-%d", errors="coerce")
# df["ACTUAL START"] = pd.to_datetime(df["ACTUAL START"], format="%Y-%m-%d", errors="coerce")

# df_melted = pd.melt(df, id_vars=["WORK ASSIGNED"], var_name="Date Type", value_name="Date")

# # Extract dates from the "Date" column
# df_melted["Date"] = pd.to_datetime(df_melted["Date"]).dt.date

# fig = make_subplots(specs=[[{"secondary_y": True}]])

# # Add bar traces for PLANNED START and ACTUAL START
# for date_type, color in zip(["PLANNED START", "ACTUAL START"], ["blue", "green"]):
#     data_df = df_melted[df_melted["Date Type"] == date_type]
#     fig.add_trace(
#         go.Bar(
#             x=data_df["WORK ASSIGNED"],
#             y=data_df["Date"],
#             name=date_type,
#             marker_color=color,
#         ),
#         secondary_y=(date_type == "ACTUAL START"),
#     )

# # Customize the layout
# fig.update_layout(
#     title="Planned Start vs Actual Start vs Work Assigned",
#     xaxis_title="Work Assigned",
#     yaxis_title="Date",
#     yaxis2_title="Date (Actual Start)",
# )

# # Display the figure in Streamlit
# st.plotly_chart(fig)