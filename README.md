# Special Offer PDF Generator

A professional Streamlit application for creating and managing special offer announcements with PDF generation capabilities.

## Features

- 📝 **Create Offers**: Generate professional offer announcements
- 💾 **SQLite Database**: Store and manage all offers locally
- 📄 **PDF Generation**: Download beautifully formatted PDF offers
- 📊 **Statistics**: Track offer metrics and analytics
- 🎨 **Professional Design**: Clean, modern interface

## Installation

1. Extract the zip file
2. Navigate to the project directory:
```bash
cd special_offer_generator
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Use the sidebar to navigate between:
   - **Create Offer**: Generate new offers
   - **View Saved Offers**: Browse and manage existing offers
   - **Statistics**: View offer analytics

## Features Overview

### Create Offer
- Enter company information (name and address)
- Add product details (name and rate)
- Set offer validity period (start and end dates)
- Generate professional PDF documents

### View Saved Offers
- Browse all saved offers in an organized format
- Download PDFs for any saved offer
- Delete unwanted offers
- Search and filter functionality

### Statistics
- View total number of offers
- See average offer rates
- Track active vs expired offers
- Recent offers overview

## Database Schema

The application uses SQLite with the following table structure:

```sql
CREATE TABLE offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    company_address TEXT,
    product_name TEXT,
    rate REAL,
    start_date TEXT,
    end_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## PDF Features

Generated PDFs include:
- Company header with name and address
- Professional styling with colors and formatting
- Offer details in structured layout
- Call-to-action sections
- Validity period footer

## Requirements

- Python 3.7+
- Streamlit 1.28.0+
- fpdf2 2.7.4+
- SQLite3 (built-in with Python)

## File Structure

```
special_offer_generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── offers.db          # SQLite database (created automatically)
└── .gitignore         # Git ignore file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue in the repository or contact the development team.
# reportappmedghor
