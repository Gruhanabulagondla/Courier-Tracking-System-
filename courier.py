import sqlite3

DATABASE = "courier_tracking.db"


# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def connect():
    return sqlite3.connect(DATABASE)


# -------------------------------
# CREATE TABLE
# -------------------------------
def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS couriers (
            courier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            sender_name TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            courier_type TEXT NOT NULL,
            weight REAL NOT NULL,
            status TEXT DEFAULT 'Booked'
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# ADD SAMPLE COURIERS
# -------------------------------
def add_sample_couriers():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM couriers")
    count = cursor.fetchone()[0]

    if count == 0:
        couriers = [
            (
                "CR1001",
                "Ravi",
                "Anjali",
                "Hyderabad",
                "Bangalore",
                "Express",
                2.5,
                "Shipped"
            ),
            (
                "CR1002",
                "Kiran",
                "Sneha",
                "Chennai",
                "Hyderabad",
                "Standard",
                1.5,
                "Out for Delivery"
            )
        ]

        cursor.executemany("""
            INSERT INTO couriers
            (tracking_id, sender_name, receiver_name,
             source, destination, courier_type,
             weight, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, couriers)

        conn.commit()

    conn.close()


# -------------------------------
# ADD COURIER
# -------------------------------
def add_courier():

    sender = input("Enter sender name: ")
    receiver = input("Enter receiver name: ")
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    courier_type = input("Enter courier type (Express/Standard): ")
    weight = float(input("Enter package weight (kg): "))

    conn = connect()
    cursor = conn.cursor()

    # Generate tracking ID
    cursor.execute("SELECT COUNT(*) FROM couriers")
    count = cursor.fetchone()[0]

    tracking_id = "CR" + str(1001 + count)

    cursor.execute("""
        INSERT INTO couriers
        (tracking_id, sender_name, receiver_name,
         source, destination, courier_type,
         weight, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tracking_id,
        sender,
        receiver,
        source,
        destination,
        courier_type,
        weight,
        "Booked"
    ))

    conn.commit()

    print("\nCourier added successfully!")
    print("Tracking ID:", tracking_id)
    print("Status: Booked")

    conn.close()


# -------------------------------
# VIEW ALL COURIERS
# -------------------------------
def view_couriers():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM couriers")
    couriers = cursor.fetchall()

    print("\n--- Courier Details ---")

    if not couriers:
        print("No courier records found.")
    else:
        for courier in couriers:
            print(
                f"ID: {courier[0]} | "
                f"Tracking ID: {courier[1]} | "
                f"Sender: {courier[2]} | "
                f"Receiver: {courier[3]} | "
                f"Route: {courier[4]} -> {courier[5]} | "
                f"Type: {courier[6]} | "
                f"Weight: {courier[7]} kg | "
                f"Status: {courier[8]}"
            )

    conn.close()


# -------------------------------
# TRACK COURIER
# -------------------------------
def track_courier():

    tracking_id = input("Enter Tracking ID: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM couriers
        WHERE tracking_id = ?
    """, (tracking_id,))

    courier = cursor.fetchone()

    if courier:
        print("\n--- Courier Tracking Details ---")
        print("Tracking ID:", courier[1])
        print("Sender:", courier[2])
        print("Receiver:", courier[3])
        print("Source:", courier[4])
        print("Destination:", courier[5])
        print("Courier Type:", courier[6])
        print("Weight:", courier[7], "kg")
        print("Status:", courier[8])
    else:
        print("Courier not found.")

    conn.close()


# -------------------------------
# UPDATE STATUS
# -------------------------------
def update_status():

    tracking_id = input("Enter Tracking ID: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM couriers
        WHERE tracking_id = ?
    """, (tracking_id,))

    courier = cursor.fetchone()

    if not courier:
        print("Courier not found.")
        conn.close()
        return

    print("\nSelect New Status")
    print("1. Booked")
    print("2. Shipped")
    print("3. Out for Delivery")
    print("4. Delivered")

    choice = input("Enter choice: ")

    status_list = {
        "1": "Booked",
        "2": "Shipped",
        "3": "Out for Delivery",
        "4": "Delivered"
    }

    if choice not in status_list:
        print("Invalid choice.")
        conn.close()
        return

    new_status = status_list[choice]

    cursor.execute("""
        UPDATE couriers
        SET status = ?
        WHERE tracking_id = ?
    """, (new_status, tracking_id))

    conn.commit()

    print("Courier status updated successfully.")
    print("New Status:", new_status)

    conn.close()


# -------------------------------
# SEARCH BY RECEIVER
# -------------------------------
def search_receiver():

    receiver = input("Enter receiver name: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM couriers
        WHERE LOWER(receiver_name) LIKE LOWER(?)
    """, ("%" + receiver + "%",))

    couriers = cursor.fetchall()

    print("\n--- Search Results ---")

    if not couriers:
        print("No courier found.")
    else:
        for courier in couriers:
            print(
                f"Tracking ID: {courier[1]} | "
                f"Receiver: {courier[3]} | "
                f"Destination: {courier[5]} | "
                f"Status: {courier[8]}"
            )

    conn.close()


# -------------------------------
# DELETE COURIER
# -------------------------------
def delete_courier():

    tracking_id = input("Enter Tracking ID: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM couriers
        WHERE tracking_id = ?
    """, (tracking_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Courier record deleted successfully.")
    else:
        print("Courier not found.")

    conn.close()


# -------------------------------
# MAIN MENU
# -------------------------------
def main():

    create_table()
    add_sample_couriers()

    while True:

        print("\n================================")
        print("     COURIER TRACKING SYSTEM")
        print("================================")
        print("1. Add Courier")
        print("2. View All Couriers")
        print("3. Track Courier")
        print("4. Update Courier Status")
        print("5. Search by Receiver")
        print("6. Delete Courier")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_courier()

        elif choice == "2":
            view_couriers()

        elif choice == "3":
            track_courier()

        elif choice == "4":
            update_status()

        elif choice == "5":
            search_receiver()

        elif choice == "6":
            delete_courier()

        elif choice == "7":
            print("Thank you for using Courier Tracking System!")
            break

        else:
            print("Invalid choice. Please try again.")


main()