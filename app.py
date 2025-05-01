import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(layout="wide")
st.title("🧠 Post-COVID Mental Health Dashboard")

# Load data
survey = pd.read_csv("data/survey.csv")
suicide = pd.read_csv("data/Crude suicide rates.csv")

# Clean column names for the suicide dataset
suicide.columns = suicide.columns.str.strip().str.lower()


# DEBUG: See actual column names (this helps in case of crashes)
st.sidebar.write("Suicide Columns:", suicide.columns.tolist())

# Fix column name if needed
if 'sex' in suicide.columns:
    suicide.rename(columns={'sex': 'gender'}, inplace=True)

# Confirm 'gender' exists before modifying
if 'gender' in suicide.columns:
    suicide['gender'] = suicide['gender'].astype(str).str.strip().str.title()

# --- Sidebar Filters ---
st.sidebar.header("Filter Suicide Data")
selected_gender = st.sidebar.selectbox("Select Gender", suicide['gender'].unique())
age_columns = [col for col in suicide.columns if 'age_' in col]
selected_age_group = st.sidebar.selectbox("Select Age Group", age_columns)

# Filtered suicide data
filtered_suicide = suicide[suicide['gender'] == selected_gender].sort_values(by=selected_age_group, ascending=False).head(10)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📈 Suicide Insights", "📋 Survey Correlation", "🔎 Raw Data"])

# --- Tab 1 ---
with tab1:
    st.subheader(f"Top 10 Countries by Suicide Rate ({selected_age_group.replace('_', ' ').title()}) - {selected_gender}")
    fig = px.bar(
        filtered_suicide,
        x=selected_age_group,
        y='country',
        orientation='h',
        color=selected_age_group,
        color_continuous_scale='Turbo',
        labels={selected_age_group: 'Suicide Rate', 'country': 'Country'},
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2 ---
with tab2:
    st.subheader("Survey Feature Correlation Heatmap")
    survey_clean = survey.select_dtypes(include=['int64', 'float64'])
    corr = survey_clean.corr().round(2)
    fig2 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title='Survey Correlation Matrix')
    st.plotly_chart(fig2, use_container_width=True)

# --- Tab 3 ---
with tab3:
    st.subheader("Raw Data Preview")
    st.dataframe(filtered_suicide)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard created with Streamlit + Plotly")
