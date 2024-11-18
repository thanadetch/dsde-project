import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils import get_df_from_csv
from dashboard import Dashboard

data_path = "data_visualization/documents_output/part-00000-e0abf9f5-4161-4b09-b8b0-e555126f4fbe-c000.csv"
data_df = get_df_from_csv(data_path)
dashboard = Dashboard(data_df)

# Set up the page configuration
st.set_page_config(page_title="Data Visualization Dashboard", layout="centered")

# Dashboard Title
st.title("Enhanced Data Visualization Dashboard")

# Arrange visualizations with wide columns
st.subheader("Overview of Key Data Insights")

dashboard.publication_counts_by_year()

dashboard.top_keywords()

dashboard.top_affiliation_countries()

dashboard.word_cloud_of_titles()

dashboard.top_publishers_by_number_of_publications()

dashboard.publisher_activity_over_time()

dashboard.data_table_preview()
