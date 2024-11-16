import streamlit as st
from pandas import DataFrame
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from visualization.utils import transform_data


class Dashboard:
    def __init__(self, df: DataFrame):
        self.df = transform_data(df)

    def publication_counts_by_year(self):
        st.subheader("Publication Counts by Year")
        pub_year = self.df['publication_date'].dt.year.value_counts().sort_index()
        st.bar_chart(pub_year)

    def top_keywords(self):
        st.subheader("Top 10 Keywords")
        all_keywords = self.df['keywords'].dropna().str.split(';').explode().str.strip()
        keyword_counts = all_keywords.value_counts().head(10)
        st.bar_chart(keyword_counts)

    def top_affiliation_countries(self):
        st.subheader("Top 10 Affiliation Countries")
        aff_countries = self.df['affiliation_countries'].dropna().str.split(';').explode().str.strip()
        country_counts = aff_countries.value_counts().head(10)
        st.bar_chart(country_counts)

    def word_cloud_of_titles(self):
        st.subheader("Word Cloud of Titles")
        title_text = ' '.join(self.df['title'].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(title_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

    def publisher_activity_over_time(self):
        st.subheader("Publisher Activity Over Time (Top 5 Publishers)")
        # Group by year and publisher, then select the top 5 publishers
        publisher_activity = self.df.groupby([self.df['publication_date'].dt.year, 'publisher']).size().unstack(
            fill_value=0)
        top_publishers = publisher_activity[list(publisher_activity.sum().nlargest(5).index)]

        # Plot the line chart with improved formatting
        fig, ax = plt.subplots(figsize=(12, 6))  # Increase width for better readability
        top_publishers.plot(ax=ax, marker='o', linestyle='-', linewidth=2)

        # Customizing the chart
        ax.set_title("Publisher Activity Over Time (Top 5 Publishers)", fontsize=14)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Number of Publications", fontsize=12)
        ax.legend(title="Publishers", title_fontsize=12, fontsize=10)

        # Adjust x-axis to show labels for specific years only
        ax.set_xticks(top_publishers.index[::2])  # Show every other year
        plt.xticks(rotation=45)  # Rotate labels for better readability

        # Add a grid for easier tracing of values
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Display the chart in Streamlit
        st.pyplot(fig)

    def top_publishers_by_number_of_publications(self):
        # Get the top 10 publishers by number of publications
        publisher_counts = self.df['publisher'].value_counts()
        top_10_publishers = publisher_counts.head(10)

        # Display the title and description above the pie chart
        st.subheader("Top 10 Publishers by Number of Publications")

        # Plot the pie chart without the legend
        fig, ax = plt.subplots(figsize=(8, 8))
        top_10_publishers.plot.pie(autopct='%1.1f%%', ax=ax, legend=False)
        ax.set_ylabel("")  # Remove the y-axis label for a cleaner look
        ax.set_title("Top 10 Publishers by Number of Publications",
                     fontsize=14)  # Add title to the chart itself for clarity

        # Display the chart in Streamlit
        st.pyplot(fig)

    def data_table_preview(self):
        st.subheader("Data Preview")
        st.write("Here’s a sample of the data:")
        st.dataframe(self.df.head(20))
