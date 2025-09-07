import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")


import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder



import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# -----------------------------
# Generate some sample data
# -----------------------------
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=100)
sales = np.random.randint(50, 200, size=100)
profit = np.random.randint(10, 100, size=100)
region = np.random.choice(["North", "South", "East", "West"], size=100)

df = pd.DataFrame({
    "Date": dates,
    "Sales": sales,
    "Profit": profit,
    "Region": region
})

# -----------------------------
# Dashboard Layout
# -----------------------------
st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 Business Dashboard")

# KPI values
total_sales = df["Sales"].sum()
avg_profit = df["Profit"].mean()
max_sales_day = df.loc[df["Sales"].idxmax(), "Date"].strftime("%Y-%m-%d")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,}")
col2.metric("Average Profit", f"${avg_profit:.2f}")
col3.metric("Best Sales Day", max_sales_day)

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------

# Sales over time
fig_sales = px.line(df, x="Date", y="Sales", title="Sales Over Time")
st.plotly_chart(fig_sales, use_container_width=True)

# Profit by region
fig_profit = px.bar(
    df.groupby("Region", as_index=False)["Profit"].mean(),
    x="Region", y="Profit",
    title="Average Profit by Region"
)
st.plotly_chart(fig_profit, use_container_width=True)

# Scatter plot of sales vs profit
fig_scatter = px.scatter(df, x="Sales", y="Profit", color="Region",
                         size="Profit", hover_data=["Date"],
                         title="Sales vs Profit by Region")
st.plotly_chart(fig_scatter, use_container_width=True)


with st.form(key="my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")
if submitted:
    st.write(f"Name: {name}, Age: {age}")


# Sample hierarchical data: Region -> Country -> City
data = {
    'Region': ['North America', 'North America', 'Europe', 'Europe', 'Asia', 'Asia'],
    'Country': ['USA', 'Canada', 'Germany', 'France', 'China', 'Japan'],
    'City': ['New York', 'Toronto', 'Berlin', 'Paris', 'Beijing', 'Tokyo'],
    'Sales': [1000, 800, 1200, 900, 1100, 950],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Streamlit app title
st.title('Hierarchical Bar Chart in Streamlit')

# Show the data
st.subheader('Raw Data:')
st.write(df)

# Create the bar chart with a 3-level hierarchy
fig = px.bar(df, x='Sales', y='City', color='Country',
             facet_col='Region', # Facet by Region
             title="Sales by City, Country, and Region",
             labels={'Sales': 'Sales ($)', 'City': 'City'},
             category_orders={
                 'Region': ['North America', 'Europe', 'Asia'],
                 'Country': ['USA', 'Canada', 'Germany', 'France', 'China', 'Japan'],
                 'City': ['New York', 'Toronto', 'Berlin', 'Paris', 'Beijing', 'Tokyo']
             })

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)



# Example data: Categories, Subcategories, and Values
data = {
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
    'Subcategory': ['Phones', 'Laptops', 'Tablets', 'Sofas', 'Tables', 'Chairs', 'Shirts', 'Jeans'],
    'Value': [100, 200, 150, 50, 120, 130, 90, 80],
    'Frequency': [5, 8, 7, 3, 6, 6, 4, 5]  # Frequency count for each item
}

# Create DataFrame
df = pd.DataFrame(data)

# Configure AgGrid for pivot table
st.title('Pivot Table with st-aggrid and Histogram')

# Set up grid options with `AgGrid`
grid_options_builder = GridOptionsBuilder.from_dataframe(df)
grid_options_builder.configure_pagination(paginationPageSize=10)  # Enable pagination
grid_options = grid_options_builder.build()

# Display the grid
st.write("Interactive Pivot Table:")
grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

# Get the filtered/aggregated data from the grid
filtered_df = grid_response['data']  # The data after pivoting or filtering

# Plot a histogram using Plotly based on the filtered data
st.write("Histogram of Values:")
histogram_fig = px.histogram(filtered_df,
                              x='Value',
                              color='Category',  # Color by Category
                              title="Value Distribution by Category",
                              labels={'Value': 'Value'},
                              barmode='overlay')  # Overlay histograms
st.plotly_chart(histogram_fig)

# Example hierarchical data: Categories and Subcategories with values
data = {
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
    'Subcategory': ['Phones', 'Laptops', 'Tablets', 'Sofas', 'Tables', 'Chairs', 'Shirts', 'Jeans'],
    'Value': [100, 200, 150, 50, 120, 130, 90, 80]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a Sunburst chart using Plotly Express
fig = px.sunburst(df,
                  path=['Category', 'Subcategory'],  # Hierarchy path
                  values='Value',
                  title="Product Categories and Subcategories (Sunburst)",
                  color='Value',  # Color by values (or use another column for categorization)
                  color_continuous_scale='Viridis')  # Optional color scale

# Display the plot in Streamlit
st.plotly_chart(fig)


import pandas as pd
import plotly.express as px
import streamlit as st

# Example hierarchical data: Categories, Subcategories, and Frequencies
data = {
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
    'Subcategory': ['Phones', 'Laptops', 'Tablets', 'Sofas', 'Tables', 'Chairs', 'Shirts', 'Jeans'],
    'Value': [100, 200, 150, 50, 120, 130, 90, 80],
    'Frequency': [5, 8, 7, 3, 6, 6, 4, 5]  # Frequency count for each item
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a histogram-like visualization with facets for each subcategory
fig = px.histogram(df,
                   x='Frequency',
                   color='Subcategory',
                   facet_col='Category',  # Facet by category
                   title="Hierarchical Histogram with Facets",
                   labels={'Frequency': 'Count of Items'},
                   barmode='stack')  # Stack bars for each subcategory

# Display the plot in Streamlit
st.plotly_chart(fig)

import pandas as pd
import plotly.express as px
import streamlit as st

# Example hierarchical data
data = {
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
    'Subcategory': ['Phones', 'Laptops', 'Tablets', 'Sofas', 'Tables', 'Chairs', 'Shirts', 'Jeans'],
    'Value': [100, 200, 150, 50, 120, 130, 90, 80]
}

# Create DataFrame
df = pd.DataFrame(data)

# Create a Treemap chart using Plotly Express
fig = px.treemap(df,
                 path=['Category', 'Subcategory'],  # Hierarchical path
                 values='Value',
                 title="Treemap for Product Categories and Subcategories",
                 color='Value',  # Color by value size
                 color_continuous_scale='Viridis')  # Color scale

# Display the plot in Streamlit
st.plotly_chart(fig)


st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Example data
np.random.seed(0)
data = pd.DataFrame({
    'values': np.random.randn(1000),
    'time': np.tile(range(1, 6), 200)
})

# Create the animated histogram
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=data['values'],
    nbinsx=30,
    name="Histogram",
    frame=dict(duration=500, redraw=True),
    visible=True
))

fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(
            label="Play",
            method="animate",
            args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]
        )]
    )],
    sliders=[dict(
        steps=[dict(
            label=str(i),
            method="animate",
            args=[[str(i)], dict(frame=dict(duration=500, redraw=True), mode="immediate")])
            for i in range(1, 6)
        ]
    )]
)

fig.update_traces(histnorm='percent')

fig.show()


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# Example data: Categories, Subcategories, and Values
data = {
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Furniture', 'Furniture', 'Furniture', 'Clothing', 'Clothing'],
    'Subcategory': ['Phones', 'Laptops', 'Tablets', 'Sofas', 'Tables', 'Chairs', 'Shirts', 'Jeans'],
    'Value': [100, 200, 150, 50, 120, 130, 90, 80],
    'Frequency': [5, 8, 7, 3, 6, 6, 4, 5]  # Frequency count for each item
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a Pivot Table
pivot_df = df.pivot_table(index='Category', columns='Subcategory', values='Value', aggfunc='sum')

# Create a Heatmap from Pivot Table (visualizing pivoted data as a table)
heatmap_fig = go.Figure(go.Heatmap(
    z=pivot_df.values,
    x=pivot_df.columns,
    y=pivot_df.index,
    colorscale='Viridis',  # Color scale
    colorbar=dict(title="Sum of Values"),
))

# Display the Pivot Table Heatmap in Streamlit
st.plotly_chart(heatmap_fig)

# Create a Histogram based on 'Value'
histogram_fig = px.histogram(df,
                              x='Value',
                              color='Category',  # Group by Category
                              title="Value Distribution by Category",
                              labels={'Value': 'Value'},
                              barmode='overlay')  # Overlay histograms

# Display the Histogram
st.plotly_chart(histogram_fig)

