"""Medghor Focus Item PDF Generator - Main Application"""
import streamlit as st
from datetime import datetime
from utils.database import init_db
from components.ui_components import (
    render_sidebar,
    render_product_form,
    render_quick_add,
    render_product_list,
    render_generate_pdf_section,
    render_saved_reports,
    render_footer
)

# Page configuration
st.set_page_config(
    page_title="Medghor Focus Item PDF Generator", 
    layout="wide"
)

# Initialize database
init_db()

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = []

if 'show_reports' not in st.session_state:
    st.session_state.show_reports = False

# Main title
st.title("📄 Medghor.com Focus Item PDF Generator")
st.markdown("Create professional focus item category reports")

# Render sidebar and get configuration
start_date, end_date, brand_name, rate_label = render_sidebar(
    datetime(2025, 10, 7),
    datetime(2025, 10, 10)
)

# Main content area
if st.session_state.show_reports:
    # Show saved reports view
    render_saved_reports(rate_label)
else:
    # Show product entry interface
    st.header("Product Details")
    
    # Product addition form
    render_product_form(rate_label)
    
    # Quick add from popular products
    render_quick_add()
    
    # Display current products
    render_product_list()
    
    # Generate PDF section
    render_generate_pdf_section(start_date, end_date, brand_name, rate_label)

# Footer
render_footer()
