import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(layout="wide")
st.title("🧠 Post-COVID Mental Health Dashboard")

# Load data
survey = pd.read_csv("data/survey.csv")
suicide = pd.read_csv("data/Crude suicide rates.csv")


suicide.rename(columns={'sex': 'gender'}, inplace=True)
suicide['gender'] = suicide['gender'].str.strip().str.title()


# --- Sidebar Filters ---
st.sidebar.header("Filter Suicide Data")
selected_gender = st.sidebar.selectbox("Select Gender", suicide['gender'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", [col for col in suicide.columns if 'age_' in col])

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
    st.write("Filtered Suicide Dataset")
    st.dataframe(filtered_suicide)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard by YOU 😎 using Streamlit + Plotly")
