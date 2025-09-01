# Hotel Management System

A desktop application for managing hotel guests, built with Python and Tkinter.  
Features include guest registration, database storage, and QR code generation/scanning for guest details.

## Features

- Add new guests with name, room number, check-in, and check-out dates
- Store guest information in a MySQL database
- View all guests in a table
- Generate QR codes for guest details
- Scan QR codes from image files to retrieve guest information

## Requirements

- Python 3.x
- MySQL server
- The following Python packages:
  - `mysql-connector-python`
  - `qrcode`
  - `Pillow`
  - `opencv-python`
  - `tkinter` (usually included with Python)

Install dependencies with:

```sh
pip install mysql-connector-python qrcode Pillow opencv-python
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/hotel-management-system.git
   cd hotel-management-system
   ```

2. **Set up the MySQL database:**
   - Create a database named `hotel_db`
   - Create a table named `guests`:
     ```sql
     CREATE TABLE guests (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255),
         room_number VARCHAR(50),
         check_in DATE,
         check_out DATE
     );
     ```
   - Update the database credentials in [`hotel management.py`](hotel%20management.py) if needed.

3. **Run the application:**
   ```sh
   python "hotel management.py"
   ```

## Usage

- Fill in guest details and click "Add Guest"
- Select a guest and click "Generate QR for Selected Guest" to create a QR code
- Click "Scan QR Code from File" to decode a QR code image

## License

MIT License

---

**Note:**  
Make sure your MySQL server is running and accessible with the credentials provided in the
