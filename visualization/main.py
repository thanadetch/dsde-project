import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import seaborn as sns

def explode_semi_colon_separated_serie(keyword_serie):
    keyword_serie = keyword_serie[keyword_serie.apply(lambda x: isinstance(x, str))]
    return (item.strip() for s in keyword_serie for item in s.split(";"))


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
        keywords_string = " ".join(explode_semi_colon_separated_serie(df["keywords"]))
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
        countries = explode_semi_colon_separated_serie(df["affiliation_countries"])
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

    def show(self):
        st.title("Data Visualization")

        st.text(f"{len(self.df):,} rows\n {len(self.df.columns):,} columns")
        st.text("Columns:")
        columns_str = "\n".join(
            [f"{i+1}. {col}" for i, col in enumerate(self.df.columns)]
        )
        st.write(columns_str)
        st.write(self.df.dtypes)

        st.text("Data table:")
        st.write(self.df)

        st.markdown("---")

        # Word Cloud for Keywords
        st.subheader("Word Cloud for Keywords")
        self.plot_wordcloud(self.df)

        # Document Count by Country
        # st.subheader("Document Count by Affiliation Country")
        # self.plot_document_count_by_country(self.df)

        # Document Count by City
        # st.subheader("Document Count by Affiliation City")
        # self.plot_document_count_by_city(self.df)

        # Document Count by Publisher
        # st.subheader("Document Count by Publisher")
        # self.plot_document_count_by_publisher(self.df)

        # Affiliation Country Distribution
        st.subheader("Document Count by Affiliation Countries")
        self.plot_affiliation_country_distribution(self.df)
        st.markdown("---")

        # Publication Date Distribution
        st.subheader("Document Count by Publication Year")
        self.plot_publication_date_distribution(self.df)
        st.markdown("---")

        # Correlation Heatmap (for numerical data)
        # st.subheader("Correlation Heatmap (if applicable)")
        # self.plot_correlation_heatmap(self.df)


# Data loading and dashboard initialization
DATA_PATH = (
    "project/documents_output/part-00000-e0abf9f5-4161-4b09-b8b0-e555126f4fbe-c000.csv"
)
df = pd.read_csv(DATA_PATH, on_bad_lines="skip", engine="python")

dashboard = DashBoard(df)
dashboard.show()
