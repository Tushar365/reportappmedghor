"""Reusable UI components for Medghor app"""
import streamlit as st
from datetime import datetime
import json
from utils.database import get_popular_products, delete_report, load_report
from utils.pdf_generator import generate_pdf

def render_sidebar(default_start, default_end):
    """Render sidebar configuration options
    
    Returns:
        tuple: (start_date, end_date, brand_name, rate_label)
    """
    st.sidebar.header("Report Configuration")
    
    # Date range
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", default_start)
    with col2:
        end_date = st.date_input("End Date", default_end)
    
    # Brand selection
    brand_type = st.sidebar.selectbox(
        "Brand Type",
        ["GENERIC FOCUS BRAND", "PHARMA FOCUS BRAND", "CUSTOM BRAND"]
    )
    
    if brand_type == "CUSTOM BRAND":
        custom_brand = st.sidebar.text_input("Enter Brand Name")
        brand_name = custom_brand if custom_brand else "CUSTOM BRAND"
    else:
        brand_name = brand_type
    
    # Rate/Discount label
    rate_label = st.sidebar.text_input("Column Label", value="Rate/Discount", 
                                       help="Customize the column header")
    
    st.sidebar.markdown("---")
    st.sidebar.header("📊 Quick Actions")
    
    # Load saved reports button
    if st.sidebar.button("📂 View Saved Reports"):
        st.session_state.show_reports = True
    
    return start_date, end_date, brand_name, rate_label

def render_product_form(rate_label):
    """Render product addition form
    
    Args:
        rate_label: Label for the rate/discount field
    """
    with st.form("add_product_form"):
        st.subheader("Add New Product")
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            product_name = st.text_input("Product Name", 
                                        placeholder="e.g., AZINTAS 500MG TAB (1*5)")
        
        with col2:
            rate_discount = st.text_input(rate_label, 
                                         placeholder="e.g., 39/- NET or 15% @ 9+1")
        
        with col3:
            st.write("")
            st.write("")
            add_button = st.form_submit_button("➕ Add", use_container_width=True)
        
        if add_button and product_name and rate_discount:
            st.session_state.products.append({
                'name': product_name,
                'rate': rate_discount
            })
            st.success(f"Added: {product_name}")

def render_quick_add():
    """Render quick add section for popular products"""
    with st.expander("⚡ Quick Add from Popular Products"):
        popular = get_popular_products(10)
        if popular:
            cols = st.columns(2)
            for idx, (prod_name, last_rate, usage_count) in enumerate(popular):
                with cols[idx % 2]:
                    if st.button(f"{prod_name} ({last_rate}) - Used {usage_count}x", 
                               key=f"quick_{idx}"):
                        st.session_state.products.append({
                            'name': prod_name,
                            'rate': last_rate
                        })
                        st.rerun()
        else:
            st.info("No products saved yet. Add some products to see them here!")

def render_product_list():
    """Display current products with delete option"""
    if st.session_state.products:
        st.subheader("Current Products")
        
        for idx, product in enumerate(st.session_state.products):
            col1, col2, col3, col4 = st.columns([0.5, 3, 2, 0.5])
            
            with col1:
                st.write(f"**{idx + 1}**")
            with col2:
                st.write(product['name'])
            with col3:
                st.write(product['rate'])
            with col4:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.products.pop(idx)
                    st.rerun()
        
        # Clear all button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear All Products", type="secondary", 
                        use_container_width=True):
                st.session_state.products = []
                st.rerun()

def render_generate_pdf_section(start_date, end_date, brand_name, rate_label):
    """Render PDF generation section with download button
    
    Args:
        start_date: Start date for the report
        end_date: End date for the report
        brand_name: Brand name for the report
        rate_label: Label for rate/discount column
    """
    from utils.database import save_report
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("📥 Generate PDF", type="primary", use_container_width=True):
            if not st.session_state.products:
                st.error("Please add at least one product before generating PDF")
            else:
                with st.spinner("Generating PDF..."):
                    pdf_buffer = generate_pdf(start_date, end_date, brand_name, 
                                             st.session_state.products, rate_label)
                    
                    # Save to database
                    save_report(start_date, end_date, brand_name, 
                              st.session_state.products)
                    
                    st.success("✅ PDF Generated and Saved Successfully!")
                    
                    # Download button
                    st.download_button(
                        label="💾 Download PDF",
                        data=pdf_buffer,
                        file_name=f"Medghor_Focus_Items_{start_date.strftime('%d%m%Y')}_{end_date.strftime('%d%m%Y')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

def render_saved_reports(rate_label):
    from utils.database import get_all_reports
    import streamlit as st
    import json
    from datetime import datetime
    st.markdown("---")
    st.header("📂 Saved Reports")
    reports = get_all_reports()
    if reports:
        for report in reports:
            report_id, start, end, brand, products_json, user_id, created = report
            products = json.loads(products_json)
            with st.expander(f"Report #{report_id} - {brand} ({start} to {end}) - {len(products)} products"):
                st.write(f"**Created:** {created}")
                st.write(f"**Date Range:** {start} to {end}")
                st.write(f"**Brand:** {brand}")
                st.write(f"**Products:** {len(products)}")
                for idx, prod in enumerate(products, 1):
                    st.write(f"{idx}. {prod['name']} - {prod['rate']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    start_dt = datetime.strptime(start, '%Y-%m-%d')
                    end_dt = datetime.strptime(end, '%Y-%m-%d')
                    from utils.pdf_generator import generate_pdf
                    pdf_buffer = generate_pdf(start_dt, end_dt, brand, products, rate_label)
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_buffer,
                        file_name=f"Medghor_Report_{report_id}.pdf",
                        mime="application/pdf",
                        key=f"download_{report_id}"
                    )

                with col2:
                    if st.button("♻️ Load to Editor", key=f"load_{report_id}"):
                        st.session_state.products = products
                        st.session_state.show_reports = False
                        st.rerun()
                with col3:
                    from utils.database import delete_report
                    if st.button("🗑️ Delete", key=f"del_{report_id}", type="secondary"):
                        delete_report(report_id)
                        st.rerun()
    else:
        st.info("No saved reports yet. Generate your first report!")
    if st.button("✖️ Close Reports View"):
        st.session_state.show_reports = False
        st.rerun()

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Medghor.com Focus Item PDF Generator | Powered by Streamlit | Made by Tushar"
        "© 2025 Medghor. All rights reserved."
        "</div>",
        unsafe_allow_html=True
    )
