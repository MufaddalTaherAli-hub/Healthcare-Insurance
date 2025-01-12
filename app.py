import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected=option_menu(
        menu_title='Menu',
        options=['Home', 'Data Analysis'],
        icons=['house', 'bar-chart'],
        default_index=0
    )


if selected == 'Home':
    from multiple_pages.predict_page import show_predict_page
    show_predict_page()
else:
    from multiple_pages.Analysis_page import show_analysis_page
    show_analysis_page()



