import streamlit as st
from streamlit_option_menu import option_menu
from analysis.financialanalysis import FinancialAnalysis

st.set_page_config(
    page_title="Financial Market Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Tweaks ---
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
        }
        h1 {
            margin-top: 0rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Financial Market Analysis Dashboard")

# --- Layout ---
col_main, col_side = st.columns([3, 1])

# --- Initialize FinancialAnalysis ---
fa = FinancialAnalysis()

with col_side:
    st.subheader("Available Stocks")

    # Current stocks
    stocks = list(fa.df_close.columns)

    # Select which to analyze
    selected_stocks = st.multiselect("Select stocks", stocks, default=stocks[:1])

    # Add new stock
    new_symbol = st.text_input("Add stock symbol (e.g. AAPL)").upper()
    if new_symbol:
        df = fa.fetch_stock(new_symbol)
        if df is not None:
            st.success(f"Added {new_symbol}")
            st.rerun()

with col_main:
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Market Overview",
            "Daily Changes",
            "Correlations",
            "Volatility",
            "More Projects"
        ],
        icons=[
            "house", "bar-chart-line", "activity", "diagram-3", "wind", "tools"
        ],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#0E1117"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#262730",
            },
            "nav-link-selected": {"background-color": "#364FBB"},
        }
    )

    # --- Dashboard Content ---
    if selected == "Home":
        st.write("Welcome to the dashboard! Select a section above.")
    elif selected == "Market Overview":
        fa.plot_prices(symbols=selected_stocks, days=200)
    elif selected == "Daily Changes":
        st.line_chart(fa.daily_changes()[selected_stocks].tail(30))
    elif selected == "Correlations":
        st.dataframe(fa.correlation_matrix().loc[selected_stocks, selected_stocks])
    elif selected == "Volatility":
        st.line_chart(fa.volatility()[selected_stocks].tail(30))
    elif selected == "More Projects":
        st.markdown("[Check my GitHub](https://github.com/minsariyasoheb)")