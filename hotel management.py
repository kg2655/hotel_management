import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import mysql.connector
import qrcode
from PIL import Image, ImageTk
import cv2
import numpy as np
import datetime

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kg_526680",
        database="hotel_db"
    )

# Insert guest into DB
def add_guest_to_db(name, room, check_in, check_out):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO guests (name, room_number, check_in, check_out) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, room, check_in, check_out))
    conn.commit()
    guest_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return guest_id

# Fetch all guests
def fetch_guests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Generate QR code for guest
def generate_qr(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

# Scan QR code from image file
def scan_qr_code(filename):
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data

# GUI Application
class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")

        # Guest form
        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky='e')
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Room Number:").grid(row=1, column=0, sticky='e')
        self.room_entry = tk.Entry(form_frame)
        self.room_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Check-in Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.checkin_entry = tk.Entry(form_frame)
        self.checkin_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Check-out Date (YYYY-MM-DD):").grid(row=3, column=0, sticky='e')
        self.checkout_entry = tk.Entry(form_frame)
        self.checkout_entry.grid(row=3, column=1)

        add_btn = tk.Button(form_frame, text="Add Guest", command=self.add_guest)
        add_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Guests list
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Room", "Check-in", "Check-out"), show='headings')
        for col in ("ID", "Name", "Room", "Check-in", "Check-out"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # QR code display
        qr_frame = tk.Frame(root)
        qr_frame.pack(pady=10)

        self.qr_label = tk.Label(qr_frame)
        self.qr_label.pack()

        # Buttons for QR code
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        gen_qr_btn = tk.Button(btn_frame, text="Generate QR for Selected Guest", command=self.generate_qr_for_selected)
        gen_qr_btn.grid(row=0, column=0, padx=5)

        scan_qr_btn = tk.Button(btn_frame, text="Scan QR Code from File", command=self.scan_qr_from_file)
        scan_qr_btn.grid(row=0, column=1, padx=5)

        self.load_guests()

    def add_guest(self):
        name = self.name_entry.get()
        room = self.room_entry.get()
        check_in = self.checkin_entry.get()
        check_out = self.checkout_entry.get()

        # Basic validation
        try:
            datetime.datetime.strptime(check_in, '%Y-%m-%d')
            datetime.datetime.strptime(check_out, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Incorrect date format, should be YYYY-MM-DD")
            return

        if not name or not room:
            messagebox.showerror("Error", "Name and Room Number are required")
            return

        guest_id = add_guest_to_db(name, room, check_in, check_out)
        messagebox.showinfo("Success", f"Guest added with ID {guest_id}")
        self.load_guests()

    def load_guests(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        guests = fetch_guests()
        for guest in guests:
            self.tree.insert('', 'end', values=guest)

    def generate_qr_for_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No guest selected")
            return
        guest = self.tree.item(selected[0])['values']
        guest_id, name, room, check_in, check_out = guest
        data = f"ID:{guest_id};Name:{name};Room:{room};CheckIn:{check_in};CheckOut:{check_out}"
        filename = f"guest_{guest_id}_qr.png"
        generate_qr(data, filename)
        img = Image.open(filename)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img_tk)
        self.qr_label.image = img_tk
        messagebox.showinfo("QR Code", f"QR code generated and saved as {filename}")

    def scan_qr_from_file(self):
        filename = filedialog.askopenfilename(title="Select QR Code Image",
                                              filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if not filename:
            return
        data = scan_qr_code(filename)
        if data:
            messagebox.showinfo("QR Code Data", f"Scanned Data:\n{data}")
        else:
            messagebox.showerror("Error", "No QR code detected or unreadable")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
