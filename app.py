import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

# -------------------- PAGE CONFIG --------------------
st.set_page_config(layout="wide")
st.title("🧠 Post-COVID Mental Health Dashboard")

# -------------------- LOAD DATA --------------------
survey = pd.read_csv("data/survey.csv")
suicide = pd.read_csv("data/Crude suicide rates.csv")

# -------------------- CLEAN SUICIDE DATA --------------------
suicide.columns = suicide.columns.str.strip().str.lower()

# Rename 'sex' to 'gender' if needed
if 'sex' in suicide.columns:
    suicide.rename(columns={'sex': 'gender'}, inplace=True)

# Clean gender column
if 'gender' in suicide.columns:
    suicide['gender'] = suicide['gender'].astype(str).str.strip().str.title()

# Detect age-related columns (like 80_above, 70to79, etc.)
age_columns = [col for col in suicide.columns if any(x in col for x in ['to', 'above'])]

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("Filter Suicide Data")
selected_gender = st.sidebar.selectbox("Select Gender", suicide['gender'].unique())

if age_columns:
    selected_age_group = st.sidebar.selectbox("Select Age Group", age_columns)
else:
    selected_age_group = None
    st.sidebar.warning("No age group columns found in suicide dataset.")

# -------------------- TABS --------------------
tab1, tab2, tab3 = st.tabs(["📈 Suicide Insights", "📋 Survey Correlation", "🔎 Raw Data"])

# -------------------- TAB 1: Suicide Insights --------------------
with tab1:
    st.subheader("Top 10 Countries by Suicide Rate")
    if selected_age_group:
        try:
            filtered_suicide = suicide[suicide['gender'] == selected_gender]
            top10 = filtered_suicide.sort_values(by=selected_age_group, ascending=False).head(10)

            fig = px.bar(
                top10,
                x=selected_age_group,
                y='country',
                orientation='h',
                color=selected_age_group,
                color_continuous_scale='Turbo',
                labels={selected_age_group: 'Suicide Rate', 'country': 'Country'},
                title=f"Top 10 Countries ({selected_gender} - {selected_age_group})"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating chart: {e}")
    else:
        st.warning("Please select a valid age group to view data.")

# -------------------- TAB 2: Survey Correlation Heatmap --------------------
with tab2:
    st.subheader("Survey Feature Correlation Heatmap")

    # Encode categorical columns for correlation
    survey_encoded = survey.copy()
    le = LabelEncoder()

    for col in survey_encoded.columns:
        if survey_encoded[col].dtype == 'object':
            try:
                survey_encoded[col] = le.fit_transform(survey_encoded[col].astype(str))
            except:
                continue  # Skip problematic columns

    survey_clean = survey_encoded.select_dtypes(include=['int64', 'float64'])

    if survey_clean.shape[1] > 1:
        corr = survey_clean.corr().round(2)
        fig2 = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale='RdBu',
            title='Survey Feature Correlation Matrix'
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Not enough numeric data in survey for correlation.")

# -------------------- TAB 3: Raw Data Preview --------------------
with tab3:
    st.subheader("Raw Suicide Data (Filtered)")
    if selected_age_group:
        st.dataframe(top10)
    else:
        st.dataframe(suicide)

# -------------------- FOOTER --------------------
st.sidebar.markdown("---")
st.sidebar.info("Dashboard built with ❤️ using Streamlit + Plotly")
