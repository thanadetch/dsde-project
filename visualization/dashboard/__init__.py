import matplotlib.pyplot as plt
import streamlit as st
from pandas import DataFrame
from wordcloud import WordCloud

from visualization.utils import transform_data


class Dashboard:
    def __init__(self, df: DataFrame):
        self.df = transform_data(df)

    def publication_counts_by_year(self):
        st.subheader("Publication Counts by Year")
        pub_year = self.df["publication_date"].dt.year.value_counts().sort_index()
        st.bar_chart(pub_year)
        description = "The trend in the number of publications has shown a consistent increase over the years, reflecting a growing interest and activity in the field. Notably, 2019 marked a significant milestone, standing out as the year with the highest number of publications, highlighting a surge in research contributions and scholarly output during that period."
        st.text(description)

    def top_keywords(self):
        st.subheader("Top 10 Keywords")
        all_keywords = self.df["keywords"].dropna().str.split(";").explode().str.strip()
        keyword_counts = all_keywords.value_counts().head(10)
        description = 'The keyword "Human" ranks highest, appearing in 4,572 documents, indicating its prominent role in the analyzed research. "Female" follows at approximately half that frequency, with "Male" close behind, emphasizing the focus on gender-related topics. The remaining keywords primarily pertain to age demographics, including "Middle Aged," "Young Adult," "Adult," and "Adolescent," which collectively reflect a strong interest in studies involving different life stages.'
        st.bar_chart(keyword_counts, color="#FFA07A")
        st.text(description)

    def top_affiliation_countries(self):
        st.subheader("Top 10 Affiliation Countries")
        aff_countries = (
            self.df["affiliation_countries"]
            .dropna()
            .str.split(";")
            .explode()
            .str.strip()
        )
        country_counts = aff_countries.value_counts().head(10)
        description = "The bar chart highlights the top 10 countries with the most research affiliations, using data sourced from the CU Office of Academic Resources. Thailand ranks first with a substantial 19,438 affiliations, far ahead of the United States with 2,696 affiliations and Japan with 1,808 affiliations. The remaining countries contribute fewer affiliations, showcasing Thailand’s dominant representation in this dataset."
        st.bar_chart(country_counts, color="#ff6b9f")
        st.text(description)

    def word_cloud_of_titles(self):
        st.subheader("Word Cloud of Titles")
        title_text = " ".join(self.df["title"].dropna().tolist())
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            title_text
        )
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        description = """The most prominent term is "Thailand," reflecting the dataset's regional focus. Other notable terms include "Effect," "Using," and "Based," which suggest a strong emphasis on methodologies and studies centered on cause-and-effect relationships. Terms like "Patient" and "Analysis" indicate a significant focus on healthcare-related research and data evaluation."""
        st.pyplot(fig)
        st.text(description)

    def publisher_activity_over_time(self):
        st.subheader("Publisher Activity Over Time (Top 5 Publishers)")
        # Group by year and publisher, then select the top 5 publishers
        publisher_activity = (
            self.df.groupby([self.df["publication_date"].dt.year, "publisher"])
            .size()
            .unstack(fill_value=0)
        )
        top_publishers = publisher_activity[
            list(publisher_activity.sum().nlargest(5).index)
        ]

        # Plot the line chart with improved formatting
        fig, ax = plt.subplots(figsize=(12, 6))  # Increase width for better readability
        top_publishers.plot(ax=ax, marker="o", linestyle="-", linewidth=2)

        # Customizing the chart
        ax.set_title("Publisher Activity Over Time (Top 5 Publishers)", fontsize=14)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Number of Publications", fontsize=12)
        ax.legend(title="Publishers", title_fontsize=12, fontsize=10)

        # Adjust x-axis to show labels for specific years only
        ax.set_xticks(top_publishers.index[::2])  # Show every other year
        plt.xticks(rotation=45)  # Rotate labels for better readability

        # Add a grid for easier tracing of values
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)

        # Display the chart in Streamlit
        st.pyplot(fig)

        description = """Elsevier Ltd leads with steady growth, peaking in 2021 and slightly declining in 2022. MDPI sees a sharp surge in 2022, surpassing other publishers. Elsevier B.V. grows gradually with a slight dip in 2022. IEEE declines after 2018 but stabilizes from 2020, while John Wiley shows steady growth. MDPI's 2022 spike likely reflects a rise in open-access publishing, highlighting Elsevier Ltd's dominance and MDPI's growing influence."""
        st.text(description)

    def top_publishers_by_number_of_publications(self):
        # Get the top 10 publishers by number of publications
        publisher_counts = self.df["publisher"].value_counts()
        top_10_publishers = publisher_counts.head(10)

        # Display the title and description above the pie chart
        st.subheader("Top 10 Publishers by Number of Publications")

        # Plot the pie chart without the legend
        fig, ax = plt.subplots(figsize=(8, 8))
        top_10_publishers.plot.pie(autopct="%1.1f%%", ax=ax, legend=False)
        ax.set_ylabel("")  # Remove the y-axis label for a cleaner look
        ax.set_title(
            "Top 10 Publishers by Number of Publications", fontsize=14
        )  # Add title to the chart itself for clarity

        # Display the chart in Streamlit
        st.pyplot(fig)

        description = "Elsevier Ltd leads with 22.8%, followed by Elsevier B.V. at 19.6%, dominating scientific, technical, and medical fields. MDPI holds 12.2% with its open-access model, while IEEE contributes 11.3% in engineering and technology. John Wiley and Sons Inc. accounts for 8.5%, covering a broad range of disciplines."
        st.text(description)

    def data_table_preview(self):
        st.subheader("Data Preview")
        st.write(
            f"The dataset containing {self.df.shape[0]:,} rows and {self.df.shape[1]:,} columns."
        )
        st.write("Sample of the data:")
        st.dataframe(self.df.head(20))
