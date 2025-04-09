import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load hypothyroidism dataset
def load_hypothyroidism_data():
    file_path = r"hypothyroidism.xlsx"  # Ensure the file is in the same directory or provide the correct path
    data = pd.read_excel(file_path)
    return data

# Load sample gene expression dataset
def load_gene_expression_data():
    # This is just a sample dataset; replace with actual gene expression data
    data = {
        "Gene": ["Gene1", "Gene2", "Gene3", "Gene4", "Gene5"],
        "Sample1": [1.2, 3.4, 2.1, 4.3, 1.5],
        "Sample2": [2.3, 4.5, 2.9, 3.6, 2.8],
        "Sample3": [1.8, 3.9, 2.7, 4.1, 1.9],
        "Sample4": [2.1, 4.0, 3.1, 3.9, 2.2],
    }
    df = pd.DataFrame(data)
    df.set_index("Gene", inplace=True)
    return df

# Main app
def main():
    # Set a scientific theme for the app
    st.set_page_config(page_title="Gene Explorer", page_icon="🧬", layout="wide")
    st.title("🧬 Gene Explorer: Hypothyroidism and Gene Expression Visualization")

    # Navigation at the top of the screen
    st.write("---")  # Add a horizontal line for separation
    app_mode = st.radio(
        "Choose the App Mode",
        ["🔬 Scientific Background", "🧬 Hypothyroidism Gene Search", "📊 Gene Expression Visualization"],
        horizontal=True,  # Display options horizontally
        label_visibility="collapsed",  # Hide the label
    )
    st.write("---")  # Add another horizontal line for separation

    if app_mode == "🔬 Scientific Background":
        st.header("🔬 Scientific Background")
        st.markdown(
            """
            ### Genetic Basis of Hypothyroidism
            Hypothyroidism is a common endocrine disorder characterized by insufficient production of thyroid hormones. 
            These hormones are crucial for regulating metabolism, growth, and development. The condition can be caused by 
            various factors, including autoimmune diseases (e.g., Hashimoto's thyroiditis), iodine deficiency, and genetic mutations.

            **Key Genes Involved:**
            - **TSHR (Thyroid Stimulating Hormone Receptor)**: Mutations in this gene can impair the thyroid gland's response to TSH, leading to hypothyroidism.
            - **PAX8 (Paired Box 8)**: This gene is essential for thyroid gland development. Mutations can result in congenital hypothyroidism.
            - **DUOX2 (Dual Oxidase 2)**: Involved in the production of hydrogen peroxide, which is necessary for thyroid hormone synthesis. Mutations can disrupt this process.

            ### Gene Expression Analysis
            Gene expression analysis is a powerful tool for understanding the molecular mechanisms underlying diseases. 
            By measuring the activity of genes across different conditions or tissues, researchers can identify biomarkers, 
            therapeutic targets, and pathways involved in disease progression.

            **Applications:**
            - **Biomarker Discovery**: Identifying genes whose expression levels correlate with disease states.
            - **Pathway Analysis**: Understanding the biological pathways affected by changes in gene expression.
            - **Drug Development**: Discovering potential drug targets based on gene expression profiles.

            This app provides tools to explore gene-related data for hypothyroidism and visualize gene expression patterns, 
            aiding in the understanding of the genetic and molecular basis of the disease.
            """
        )

    elif app_mode == "🧬 Hypothyroidism Gene Search":
        st.header("🧬 Hypothyroidism Gene Search")
        st.markdown(
            """
            **Hypothyroidism** is a condition in which the thyroid gland doesn't produce enough thyroid hormones. 
            It can affect metabolism, energy levels, and overall health. The **genetic basis** of hypothyroidism 
            includes mutations in various genes that play a role in thyroid function and development.
            
            This app allows you to explore **gene-related data** relevant to hypothyroidism. Enter a gene name 
            in the search bar to retrieve detailed information.
            """
        )

        # Load hypothyroidism data
        data = load_hypothyroidism_data()

        # Search functionality at the top
        st.header("🔍 Search for Gene Information")
        gene_name = st.text_input("Enter Gene Name:")

        # Display the image below the search bar with reduced size
        st.image("Hypothyroidism image.jpg", caption="Healthy Thyroid vs Hypothyroidism", width=400)  # Adjust width as needed

        if gene_name:
            # Filter data by gene name
            filtered_data = data[data["Gene Names"].str.contains(gene_name, case=False, na=False)]

            if not filtered_data.empty:
                st.write("### 🧬 Search Results")

                # Modify Sequence column to display as clickable links
                filtered_data = filtered_data.copy()
                filtered_data["Sequence"] = filtered_data["Sequence"].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

                # Convert DataFrame to HTML for rendering clickable links
                st.write(filtered_data.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.write("❌ No gene found with the provided name.")

    elif app_mode == "📊 Gene Expression Visualization":
        st.header("📊 Gene Expression Visualization Tool")
        st.write("""
            This tool visualizes **gene expression data** to help researchers analyze patterns and trends in gene activity. 
            Upload your gene expression data file (CSV) or use the sample dataset to explore visualizations.
        """)

        # File uploader
        uploaded_file = st.file_uploader("Upload Gene Expression Data (CSV)", type=["csv"])

        if uploaded_file is not None:
            # Load user-uploaded data
            df = pd.read_csv(uploaded_file, index_col=0)
        else:
            # Load sample data if no file is uploaded
            df = load_gene_expression_data()

        # Display dataset
        st.subheader("📂 Gene Expression Data")
        st.dataframe(df)

        # Gene expression heatmap
        st.subheader("🔥 Gene Expression Heatmap")
        st.markdown("""
            A **heatmap** is a graphical representation of data where individual values are represented by colors. 
            This heatmap shows the expression levels of genes across different samples.
        """)
        fig, ax = plt.subplots(figsize=(10, 8))  # Explicitly create a figure and axis
        sns.heatmap(df.T, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
        st.pyplot(fig)  # Pass the figure object to st.pyplot

        # Gene expression bar plot for each sample
        st.subheader("📈 Gene Expression Bar Plot")
        st.markdown("""
            A **bar plot** shows the expression levels of a selected gene across different samples.
        """)
        gene = st.selectbox("Select Gene for Bar Plot", df.index)
        st.bar_chart(df.loc[gene])

        # Gene expression line plot for each gene across samples
        st.subheader("📉 Gene Expression Line Plot")
        st.markdown("""
            A **line plot** shows the expression trends of selected genes across different samples.
        """)
        selected_genes = st.multiselect("Select Genes for Line Plot", df.index)
        if selected_genes:
            st.line_chart(df.loc[selected_genes].T)
        else:
            st.write("⚠️ Please select at least one gene to visualize.")

        # Box plot to show distribution of gene expression across samples
        st.subheader("📦 Gene Expression Distribution (Box Plot)")
        st.markdown("""
            A **box plot** shows the distribution of gene expression levels across samples, highlighting 
            the median, quartiles, and potential outliers.
        """)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df.T, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # About section at the bottom
    st.write("---")  # Add a horizontal line for separation
    st.header("About")
    st.info(
        """
        **Gene Explorer** is a scientific tool built using Streamlit. 
        It provides information about genes associated with hypothyroidism and visualizes gene expression data.
        
        - **🔬 Scientific Background**: Learn about the genetic and molecular basis of hypothyroidism and the importance of gene expression analysis.
        - **🧬 Hypothyroidism Gene Search**: Explore gene-related data for hypothyroidism.
        - **📊 Gene Expression Visualization**: Analyze gene expression patterns using heatmaps, bar plots, line plots, and box plots.
        """
    )

# Run the app
if __name__ == "__main__":
    main()
