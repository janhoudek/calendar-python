# calendar_python
Automated script to create a calendar table using Python. Allows you to generate a table with dates, complete with various time dimensions such as day of the week, month, quarter, weekdays, weekends, and more. Ideal for data warehousing and analytics applications.

This project includes predefined holiday calculations for the Czech Republic. You can customize these holidays or add additional ones as needed.

## Features

- Generate a calendar table with customizable date ranges.
- Include time dimensions such as:
  - Day of the week
  - Month
  - Quarter
  - Weekdays and weekends
  - Holidays (customizable)
- User-defined functions (UDFs) for additional date-related calculations.
- Validation utilities to ensure data consistency.

## Project Structure
calendar-python/
├── calendar_table_column_description.csv # Description of calendar table columns
├── calendar.csv # Example output calendar table
├── create_calendar.py # Main script to generate the calendar table
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── udfs/ # Directory for user-defined functions
│ ├── date_udfs.py # UDFs for date calculations
│ ├── df_udfs.py # UDFs for DataFrame operations
│ ├── easter_calculator.py # Utility to calculate Easter dates
│ ├── holidays_udfs.py # UDFs for holiday calculations
│ └── validation_udfs.py # UDFs for data validation
└── .gitignore # Git ignore rules

## Prerequisites

- Python 3.8 or higher
- Required Python libraries (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/calendar-python.git
   cd calendar-python
   ```

2. Create a virtual environment and activate it:
    ```bash
    pip install -r requirements.txt
    ```

3. Install dependencies:
    ```bash
    python create_calendar.py
    ```

## Usage
1. Run the create_calendar.py script to generate a calendar table:
    ```bash
    python create_calendar.py
    ```

2. Customize the script or UDFs in the udfs/ directory to fit your specific requirements.

Customize the script or UDFs in the udfs/ directory to fit your specific requirements.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Inspired by common data warehousing practices for calendar tables.
Special thanks to contributors and the open-source community.