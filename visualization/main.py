import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils import get_df_from_csv
from dashboard import Dashboard

data_path = "project/documents_output/part-00000-e0abf9f5-4161-4b09-b8b0-e555126f4fbe-c000.csv"
data_df = get_df_from_csv(data_path)
dashboard = Dashboard(data_df)

# Set up the page configuration
st.set_page_config(page_title="Data Visualization Dashboard", layout="centered")

# Dashboard Title
st.title("Enhanced Data Visualization Dashboard")

# Arrange visualizations with wide columns
st.subheader("Overview of Key Data Insights")

# 1. Publication Counts by Year
dashboard.publication_counts_by_year()

# 2. Top 10 Keywords with Custom Color
dashboard.top_keywords()

# 3. Top 10 Affiliation Countries with Custom Color
dashboard.top_affiliation_countries()

# 4. Word Cloud of Titles with Custom Color
dashboard.word_cloud_of_titles()

# 5. Publisher Activity Over Time with Distinct Color Lines
dashboard.publisher_activity_over_time()

# 6. Title Length Distribution with Custom Color
dashboard.title_length_distribution()

# 7. Data Table Preview
dashboard.data_table_preview()
