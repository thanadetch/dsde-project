import pandas as pd
import streamlit as st
from pandas import DataFrame
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

from visualization.utils import explode_semi_colon_separated_series, transform_data


class Dashboard:
    def __init__(self, df: DataFrame):
        self.df = transform_data(df)

    def keywords(self, df):
        keywords_string = " ".join(explode_semi_colon_separated_series(df["keywords"]))
        return keywords_string

    def plot_wordcloud(self, df):
        keywords_string = self.keywords(df)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            keywords_string
        )
        # Create a figure and pass it to st.pyplot
        fig = plt.figure(figsize=(8, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig)

    def plot_document_count_by_country(self, df):
        country_counts = df["affiliation_countries"].value_counts()
        # Create a figure and pass it to st.pyplot
        fig, ax = plt.subplots(figsize=(8, 6))
        country_counts.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Document Count by Affiliation Country")
        ax.set_xlabel("Country")
        ax.set_ylabel("Number of Documents")
        st.pyplot(fig)

    def plot_document_count_by_city(self, df):
        city_counts = df["affiliation_cities"].value_counts()
        # Create a figure and pass it to st.pyplot
        fig, ax = plt.subplots(figsize=(8, 6))
        city_counts.plot(kind="bar", color="lightgreen", ax=ax)
        ax.set_title("Document Count by Affiliation City")
        ax.set_xlabel("City")
        ax.set_ylabel("Number of Documents")
        st.pyplot(fig)

    def plot_document_count_by_publisher(self, df):
        publisher_counts = df["publisher"].value_counts()
        # Create a figure and pass it to st.pyplot
        fig, ax = plt.subplots(figsize=(8, 6))
        publisher_counts.plot(kind="bar", color="lightblue", ax=ax)
        ax.set_title("Document Count by Publisher")
        ax.set_xlabel("Publisher")
        ax.set_ylabel("Number of Documents")
        st.pyplot(fig)

    def plot_affiliation_country_distribution(self, df):
        # If there are multiple countries
        countries = explode_semi_colon_separated_series(df["affiliation_countries"])
        country_counts = pd.Series(countries).value_counts()

        # Get the top 10 countries
        top_10_countries = country_counts.head(10).sort_values(ascending=True)

        # Create a figure and pass it to st.pyplot
        fig, ax = plt.subplots(figsize=(10, 6))
        top_10_countries.plot(
            kind="barh", color="lightblue", ax=ax
        )  # horizontal bar chart
        ax.set_title("Top 10 Document Count by Affiliation Countries")
        ax.set_xlabel("Number of Documents")
        ax.set_ylabel("Country")
        st.pyplot(fig)

    def plot_publication_date_distribution(self, df):
        df["publication_year"] = df["publication_date"].dt.year
        publication_counts = df["publication_year"].value_counts().sort_index()
        # Create a figure and pass it to st.pyplot
        fig, ax = plt.subplots(figsize=(8, 6))
        publication_counts.plot(kind="bar", color="lightcoral", ax=ax)
        ax.set_title("Document Count by Publication Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Documents")
        st.pyplot(fig)

    def plot_correlation_heatmap(self, df):
        # If there are numeric columns, we can plot a correlation heatmap
        numeric_columns = df.select_dtypes(include=["number"]).columns
        if len(numeric_columns) > 0:
            corr = df[numeric_columns].corr()
            # Create a figure and pass it to st.pyplot
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

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
        ax.set_title("Top 10 Publishers by Number of Publications", fontsize=14)  # Add title to the chart itself for clarity

        # Display the chart in Streamlit
        st.pyplot(fig)

    def data_table_preview(self):
        st.subheader("Data Preview")
        st.write("Here’s a sample of the data:")
        st.dataframe(self.df.head(20))
