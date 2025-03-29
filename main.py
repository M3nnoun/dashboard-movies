import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval

# Load data
# Note: You should either use the CSV string OR read from file, not both
# Uncomment one of these approaches:
# Option 1: Load from string (replace the placeholder with actual CSV data)
# data = """YOUR CSV DATA HERE"""  # Paste your CSV data here
# df = pd.read_csv(StringIO(data))

# Option 2: Load from file (use this if your file exists)
df = pd.read_csv("sample_data.csv")

# Data cleaning
df['genres'] = df['genres'].apply(literal_eval)
df['year'] = pd.to_numeric(df['year'], errors='coerce')  # Changed to numeric instead of string
df['runtime_min'] = pd.to_numeric(df['runtime_min'], errors='coerce')

# Streamlit app
st.set_page_config(page_title="Movie Analytics Dashboard", layout="wide")
st.title("🎬 Advanced Movie Analytics Dashboard")

# ===== Key Metrics Section =====
st.header("📊 Key Statistics")
cols = st.columns(4)
with cols[0]:
    st.metric("Total Movies", len(df))
with cols[1]:
    st.metric("Avg Rating", f"{df['score'].mean():.1f}/10")
with cols[2]:
    st.metric("Avg Runtime", f"{df['runtime_min'].mean():.1f} mins")
with cols[3]:
    st.metric("Unique Genres", df.explode('genres')['genres'].nunique())

# ===== Main Visualization Tabs =====
tab1, tab2, tab3 = st.tabs(["📈 Distributions", "📊 Relationships", "🏆 Top Performers"])

with tab1:
    # Year Distribution
    st.subheader("📅 Movie Releases by Year")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    year_counts = df['year'].value_counts().sort_index()  # Sort by year
    sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax1, palette='viridis')
    ax1.set_xlabel("Release Year")
    ax1.set_ylabel("Number of Movies")
    plt.xticks(rotation=45)  # Rotate year labels
    st.pyplot(fig1)
    
    # Genre Distribution
    st.subheader("🎭 Genre Distribution")
    genre_counts = df.explode('genres')['genres'].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax2, palette='rocket')
    ax2.set_xlabel("Count")
    ax2.set_ylabel("Genre")
    st.pyplot(fig2)

with tab2:
    # Scatter Plot: Runtime vs Rating
    st.subheader("⏱️ Runtime vs Rating")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='runtime_min', y='score', 
                    hue='year', size='score', 
                    sizes=(50, 200), palette='mako', ax=ax3)
    ax3.set_xlabel("Runtime (minutes)")
    ax3.set_ylabel("IMDb Rating")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig3)
    
    # Year vs Rating
    st.subheader("📅 Year vs Rating")
    # Fix: lmplot creates its own figure, so we don't need fig4, ax4
    year_rating_plot = sns.lmplot(data=df, x='year', y='score', height=6, aspect=1.5)
    plt.xlabel("Release Year")
    plt.ylabel("IMDb Rating")
    st.pyplot(year_rating_plot)
    
    # Correlation Heatmap
    st.subheader("🔗 Feature Correlations")
    numeric_df = df[['score', 'runtime_min', 'year']].apply(pd.to_numeric, errors='coerce')
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax5)
    st.pyplot(fig5)

with tab3:
    # Top Rated Movies
    st.subheader("🌟 Top 10 Movies by Rating")
    top_movies = df[['title', 'year', 'score', 'genres']].sort_values('score', ascending=False)
    # Fix: Convert genres list to string for display
    top_movies_display = top_movies.head(10).copy()
    top_movies_display['genres'] = top_movies_display['genres'].apply(lambda x: ', '.join(x))
    st.dataframe(top_movies_display.style.background_gradient(subset=['score'], cmap='YlGn'),
                 height=400)
    
    # Genre vs Rating
    st.subheader("🏅 Top Genres by Average Rating")
    genre_scores = df.explode('genres').groupby('genres')['score'].mean().sort_values(ascending=False)
    fig6, ax6 = plt.subplots(figsize=(10, 4))
    sns.barplot(x=genre_scores.head(10).values, y=genre_scores.head(10).index, 
                palette='plasma', ax=ax6)
    ax6.set_xlabel("Average Rating")
    ax6.set_ylabel("Genre")
    st.pyplot(fig6)

# ===== Raw Data Section =====
st.header("📁 Data Exploration")
# Fix: st.expander needs to be used with a with statement
with st.expander("Show Raw Data Table"):
    # Create a display version with genres as strings
    display_df = df.copy()
    display_df['genres'] = display_df['genres'].apply(lambda x: ', '.join(x))
    st.dataframe(display_df)

# ===== Footer =====
st.markdown("---")
st.markdown("*Dashboard created with ❤️ in INSEA*")