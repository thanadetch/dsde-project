import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

from visualization.utils import explode_semi_colon_separated_series


class DashBoard:
    def __init__(self, df):
        self.df = self.transform_data(df)

    def transform_data(self, df):
        df["document_id"] = df["document_id"].astype("string")
        df["affiliation_countries"] = df["affiliation_countries"].astype("string")
        df["affiliation_cities"] = df["affiliation_cities"].astype("string")
        df["affiliation_names"] = df["affiliation_names"].astype("string")
        df["title"] = df["title"].astype("string")
        df["description"] = df["description"].astype("string")
        df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")
        df["keywords"] = df["keywords"].astype("string")
        df["publisher"] = df["publisher"].astype("string")
        return df

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
        publisher_activity = self.df.groupby([self.df['publication_date'].dt.year, 'publisher']).size().unstack(
            fill_value=0)
        top_publishers = publisher_activity[list(publisher_activity.sum().nlargest(5).index)]
        st.line_chart(top_publishers)

    def title_length_distribution(self):
        st.subheader("Title Length Distribution")
        fig, ax = plt.subplots()
        self.df['title_length'] = self.df['title'].apply(lambda x: len(x) if pd.notna(x) else 0)
        ax.hist(self.df['title_length'], bins=30, edgecolor='black')
        st.pyplot(fig)
        st.write("Below is the distribution of title lengths in characters.")

    def data_table_preview(self):
        st.subheader("Data Preview")
        st.write("Here’s a sample of the data:")
        st.dataframe(self.df.head(20))
