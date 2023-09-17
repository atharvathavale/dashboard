import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
# import ifcopenshell
# from pythreejs import *
# import streamlit.components.v1 as components

#Page heading 
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
st.title("PROJECT DASHBOARD")
# Load the CSV data
data = pd.read_csv('latest_data.csv')

see_fulldata = st.expander('To view data👉')
with see_fulldata:
    st.write(data)

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
status_counts = df['Status'].value_counts()
fig = px.pie(
        status_counts,
        names=status_counts.index,
        values=status_counts.values,
        title='Task Status Distribution'
    )
st.title('Task Status Pie Chart')
st.plotly_chart(fig)


# SECTION - PIE CHART AND TABLE ON Hinderance
df_hind = df[['Hinderance','Hinderance In','Hinderance Priority']]
st.write(df_hind)
status_counts = df['Hinderance Priority'].value_counts()
fig = px.pie(
        status_counts,
        names=status_counts.index,
        values=status_counts.values,
        title='Hinderance priority distribution'
    )
st.title('Hinderance priority distribution')
st.plotly_chart(fig)



# SECTION - DEADLINE COMING SOON  
# Convert date columns to datetime objects
df['PLANNED FINISHH'] = pd.to_datetime(df['Baseline Finish'])
# Calculate the current date
current_date = datetime.now()
# Filter rows where 'PLANNED-FINISH' is within 2 days of the current date
deadline_df = df[(( df['PLANNED FINISHH'] - current_date ).dt.days <= 2) & ((df['PLANNED FINISHH'] - current_date ).dt.days > 0)]
# Display the 'deadline_df'
# st.header('Deadline soon approaching', divider='rainbow')
st.header('Deadline soon approaching', divider='rainbow')
st.write(deadline_df[['Resource Initials','Task Name','Status','Start','Baseline Finish','Duration']].head())


#IMPACT4IMPACT LOGO
st.sidebar.image("i4ilogo.png", use_column_width=True)

# WORKS and DEADLINES CROSSED 
df_works = df['Task Name']
st.sidebar.header("Works in the project :",divider="rainbow")
st.sidebar.write(df_works)
df_crossed = df[(df['PLANNED FINISHH'] - current_date ).dt.days < 0]
st.sidebar.header('Deadlines crossed', divider='red')
st.sidebar.write(df_crossed[['Resource Initials','Task Name','Status','Start','Baseline Finish','Duration']].head())

#MODEL VIEWER
# Create a custom Streamlit component to display the 3D model

# if st.sidebar.button('MODEL'):
#     # Display the IFC model when the button is clicked
#     # Load your IFC file here (replace 'your_model.ifc' with the path to your IFC file)
#     ifc_file_path = ifcopenshell.open('building_model.ifc')
#     st.write(ifc_file_path.schema)
#     walls = ifc_file_path.by_type('IfcWall')
#     st.write(walls.get_info())
