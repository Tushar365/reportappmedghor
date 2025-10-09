"""PDF generation utilities for Medghor Focus Item reports"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


class ColorPalette:
    """Color scheme for the PDF"""
    PRIMARY_ORANGE = colors.HexColor('#FF9900')
    LIGHT_ORANGE = colors.HexColor('#FFE6CC')
    HEADER_GRAY = colors.HexColor('#CCCCCC')
    ALT_ROW_GRAY = colors.HexColor('#F5F5F5')
    TEXT_BLACK = colors.black
    WHITE = colors.white


class PDFStyles:
    """Centralized style definitions"""
    
    @staticmethod
    def get_title_style():
        """Style for main title"""
        return ParagraphStyle(
            'CustomTitle',
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=ColorPalette.TEXT_BLACK,
            spaceAfter=10,
            alignment=TA_CENTER,
            leading=20
        )
    
    @staticmethod
    def get_brand_style():
        """Style for brand name"""
        return ParagraphStyle(
            'BrandStyle',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=ColorPalette.TEXT_BLACK,
            spaceAfter=20,
            alignment=TA_CENTER
        )


def create_title_section(start_date, end_date, contact_number="1234567890"):
    """Create formatted title section with orange background
    
    Args:
        start_date: Start date of the report period
        end_date: End date of the report period
        contact_number: Contact phone number
    
    Returns:
        Table object with styled title
    """
    title_style = PDFStyles.get_title_style()
    
    title_text = (
        f"⭐⭐OFFER ITEM⭐⭐<br/>"
        f"FROM {start_date.strftime('%d.%m.%Y')} TO {end_date.strftime('%d.%m.%Y')}<br/>"
        f"CONTACT - {contact_number}"
    )
    
    title = Paragraph(title_text, title_style)
    title_table = Table([[title]], colWidths=[7.5*inch])
    
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ColorPalette.PRIMARY_ORANGE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 2, ColorPalette.TEXT_BLACK),
    ]))
    
    return title_table


def create_brand_section(brand_name):
    """Create formatted brand name section
    
    Args:
        brand_name: Brand name to display
    
    Returns:
        Table object with styled brand name
    """
    brand_style = PDFStyles.get_brand_style()
    brand = Paragraph(brand_name, brand_style)
    brand_table = Table([[brand]], colWidths=[7.5*inch])
    
    brand_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ColorPalette.LIGHT_ORANGE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, ColorPalette.TEXT_BLACK),
    ]))
    
    return brand_table


def create_product_table(products, rate_label):
    """Create formatted product table with alternating row colors
    
    Args:
        products: List of product dictionaries with 'name' and 'rate' keys
        rate_label: Custom label for the rate/discount column
    
    Returns:
        Table object with styled product data
    """
    # Prepare table data
    data = [['SL', 'PRODUCT NAME', rate_label.upper()]]
    
    for idx, product in enumerate(products, 1):
        data.append([
            str(idx),
            product.get('name', 'N/A'),
            product.get('rate', 'N/A')
        ])
    
    # Column widths: Serial (0.5"), Product Name (5"), Rate (1.5")
    col_widths = [0.5*inch, 5*inch, 1.5*inch]
    product_table = Table(data, colWidths=col_widths, repeatRows=1)
    
    # Base table styling
    table_style = [
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), ColorPalette.HEADER_GRAY),
        ('TEXTCOLOR', (0, 0), (-1, 0), ColorPalette.TEXT_BLACK),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows styling
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        
        # Alignment
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Serial number column
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Product name column
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Rate column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Borders
        ('GRID', (0, 0), (-1, -1), 1, ColorPalette.TEXT_BLACK),
        ('LINEBELOW', (0, 0), (-1, 0), 2, ColorPalette.TEXT_BLACK),
    ]
    
    # Alternate row colors for better readability
    for i in range(1, len(data)):
        bg_color = ColorPalette.ALT_ROW_GRAY if i % 2 == 0 else ColorPalette.WHITE
        table_style.append(('BACKGROUND', (0, i), (-1, i), bg_color))
    
    product_table.setStyle(TableStyle(table_style))
    return product_table


def generate_pdf(start_date, end_date, brand_name, products, rate_label, 
                 contact_number="1234567890"):
    """Generate PDF for focus item report
    
    Args:
        start_date: Start date of the report period
        end_date: End date of the report period
        brand_name: Brand name for the report
        products: List of product dictionaries with 'name' and 'rate' keys
        rate_label: Custom label for the rate/discount column
        contact_number: Contact phone number (default: "1234567890")
    
    Returns:
        BytesIO buffer containing the generated PDF
    
    Raises:
        ValueError: If products list is empty
    """
    if not products:
        raise ValueError("Products list cannot be empty")
    
    # Initialize PDF buffer and document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        title=f"Medghor Offer - {brand_name}",
        author="Medghor"
    )
    
    elements = []
    
    # Add title section
    title_table = create_title_section(start_date, end_date, contact_number)
    elements.append(title_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Add brand section
    brand_table = create_brand_section(brand_name)
    elements.append(brand_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Add product table
    product_table = create_product_table(products, rate_label)
    elements.append(product_table)
    
    # Add footer spacer
    elements.append(Spacer(1, 0.3*inch))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer


# Example usage
if __name__ == "__main__":
    from datetime import datetime
    
    # Sample data
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 31)
    brand = "HIMALAYA WELLNESS"
    products_list = [
        {"name": "Liv.52 DS Tablet 60's", "rate": "₹245"},
        {"name": "Lukol Tablet 60's", "rate": "₹180"},
        {"name": "Mentat Tablet 50's", "rate": "₹195"},
        {"name": "Cystone Tablet 60's", "rate": "₹220"},
    ]
    
    # Generate PDF
    pdf_buffer = generate_pdf(
        start_date=start,
        end_date=end,
        brand_name=brand,
        products=products_list,
        rate_label="Offer Price"
    )
    
    # Save to file
    with open("medghor_offer.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())
    
    print("PDF generated successfully!")
