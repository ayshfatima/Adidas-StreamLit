import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Load the Excel file
df = pd.read_excel("Adidas.xlsx")

# Set up the Streamlit app layout
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:2.2rem;}</style>', unsafe_allow_html = True)
# st.title("Adidas Data Explorer")
image1 = Image.open('adidas.jpg')
col1,col2 = st.columns([0.1,0.9])
with col1:
    st.image(image1, width=100)
html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Adidas Sales Insights By Ayesha</h1></center>"""
with col2:
    st.markdown(html_title,unsafe_allow_html=True)
col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last Updated On:  \n {box_date}")
with col4:
    fig = px.bar(df, x="Retailer",y="TotalSales",  labels={"Totalsales":"Total Sales"},
                 title="Total Sales By Retailer", hover_data=["TotalSales"],
                 template="gridon",height=500,color_discrete_sequence=["#6a0dad"])
    st.plotly_chart(fig, use_container_width=True)
_,view1,dwn1,view2,dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retail Wise Sales")
    
    data = df[["Retailer","TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Click Me To Download The Data",data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales", mime="text/csv")
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b '%y")
result = df.groupby(by = df["Month_Year"])["TotalSales"].sum().reset_index()
with col5:
    fig1= px.line(result,x="Month_Year",y="TotalSales",title="Total Sales Over Time",
                  template="gridon",color_discrete_sequence=["#6a0dad"],height=500)
    st.plotly_chart(fig1,use_container_width=True)
with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button ("Click Me To Download The Data",data = result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales", mime="text/csv")  
st.divider()
# Grouping the data
result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# Create a figure
fig3 = go.Figure()

# Add a bar trace for Total Sales
fig3.add_trace(
    go.Bar(
        x=result1["State"],
        y=result1["TotalSales"],
        name="Total Sales",
        marker_color = "#6a0dad"
    )
)

# Add a line trace for Units Sold, using a secondary y-axis
fig3.add_trace(
    go.Scatter(
        x=result1["State"],
        y=result1["UnitsSold"],
        mode="lines",
        name="Units Sold",
        yaxis="y2"
    )
)

# Update layout to include a secondary y-axis
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis_title="State",
    yaxis_title="Total Sales",
    yaxis2=dict(
        title="Units Sold",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.1, y=1.1)
)

_,col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)
st.divider()