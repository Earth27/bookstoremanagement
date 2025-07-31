import mysql.connector
import sys

print("Welcome to EKR-Bookstore")
print("Enter password to enter the Bookstore")
passwd = input("Enter Password: ")
try:
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        password=passwd,
        database="EKR_BookStore"
    )

    if db.is_connected():
        print("Successfully connected to the EKR Bookstore database!")

except mysql.connector.Error as err:
    print("Error: Could not connect to the database. Please check the password and try again.")
    sys.exit("Exiting program due to incorrect password.")

cursor = db.cursor()

def add_book_to_inventory():
    book_name = input("Enter Book Name: ")
    market_price = float(input("Enter Market Price: "))
    unit=int(input("Enter no. of units: "))
    query = "INSERT INTO InventoryManagement (BookName, MarketPrice, Units) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_name, market_price, unit))
    db.commit()
    print("Book", book_name, "added successfully with a price of", market_price)

def search_books(book_name):

    query = "SELECT * FROM InventoryManagement WHERE LOWER(BookName) LIKE %s"
    cursor.execute(query, ('%' + book_name.lower() + '%',))  
    results = cursor.fetchall()
    if results:
        print("Matching Books:")
        for idx, book in enumerate(results):
            print((idx + 1), "Book ID:", book[0], "Book Name:", book[1], "Market Price:", book[2])
    else:
        print("No matching books found.")

def show_all_books():
    query = "SELECT * FROM InventoryManagement"
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        print("All Books in Inventory:")
        for idx, book in enumerate(results):
            print((idx + 1), "Book ID:", book[0], "Book Name:", book[1], "Market Price:", book[2], "Units:", book[3])
    else:
        print("No books available in inventory.")


def is_valid_email(email):
    if "@" in email and "." in email.split("@")[-1]:
        return True
    return False

def search_book(book_name):
    query = "SELECT * FROM InventoryManagement WHERE LOWER(BookName) LIKE LOWER(%s)"
    cursor.execute(query, ('%' + book_name + '%',))
    results = cursor.fetchall()
    return results

def place_order():
    customer_name = input("Enter your name: ")
    email = input("Enter your email address: ")

    while not is_valid_email(email):
        print("Please enter a valid email address.")
        email = input("Enter your email address: ")

    book_name = input("Enter the book name: ")
    books = search_book(book_name)

    if books:
        print("Matching Books:")
        for idx, book in enumerate(books):
            print((idx + 1), ". Book ID:", book[0], "Book Name:", book[1], "Market Price:", book[2])

        choice = int(input("Select a book by number: ")) - 1
        
        if 0 <= choice < len(books):
            selected_book = books[choice]
            price = selected_book[2]
            check_stock_query = "SELECT Units FROM InventoryManagement WHERE BookID = %s"
            cursor.execute(check_stock_query, (selected_book[0],))
            available_units = cursor.fetchone()[0]

            if available_units > 0:
                print("\nSelected Book: ", selected_book[1], "Price: ", price)
            else:
                print("Sorry, this book is out of stock. Order cancelled.")
                return
        else:
            print("Invalid selection. Going back to previous step.")
            return
    else:
        print("No matching books found.")
        return

    while True:
        payment_method = input("Select payment method: 1 for Cash, 2 for Online Payment: ").strip()

        if payment_method == '2':
            print("Payment module is not imported yet, it will be there in nearer future")
            cancel_option = input("Press 1 to COD or 2 to Cancel order: ").strip()

            if cancel_option == '2':
                print("Order cancelled")
                return
            elif cancel_option == '1':
                payment_status = "Paid"
                break
            else:
                print("Invalid selection. Please choose a valid option.")
        elif payment_method == '1':
            payment_status = "Paid"
            break
        else:
            print("Invalid payment method. Please choose a valid option.")

    while True:
        paid_decision = input("COD - Paid (Y/N)? ").strip().lower()

        if paid_decision == 'y':
            update_query = "UPDATE InventoryManagement SET Units = Units - 1 WHERE BookID = %s"
            cursor.execute(update_query, (selected_book[0],))
            db.commit()
            query = "INSERT INTO CustomerData (CustomerName, Email, BookOrdered, BookPrice, PaymentStatus) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (customer_name, email, selected_book[1], price, payment_status))
            db.commit()

            customer_id = cursor.lastrowid

            print("Bill Details:")
            print("Customer ID:", customer_id)
            print("Customer Name:", customer_name)
            print("Contact (Email):", email)
            print("Book Ordered:", selected_book[1])
            print("Price:", price)
            print("Amount to Pay:", price)
            print("Payment Status:", payment_status)

            print("Thanks for your purchase!")
            break
        elif paid_decision == 'n':
            print("Please confirm your payment again.")
        else:
            print("Invalid input. Please enter 'Y' for Paid or 'N' to go back.")

    again = input("Do you want to add another order? (Y/N): ").strip().lower()
    if again == 'y':
        place_order()
    else:
        main_menu()
 
def show_transactions_details(customer_id=None, contact=None):
    if customer_id:
        query = "SELECT * FROM CustomerData WHERE CustomerID = %s"
        cursor.execute(query, (customer_id,))
    elif contact:
        query = "SELECT * FROM CustomerData WHERE Email = %s"
        cursor.execute(query, (contact,))

    results = cursor.fetchall()

    if not results:
        if customer_id:
            print("\nNo records found for Customer ID:", customer_id)
        elif contact:
            print("\nNo records found for Email ID:", contact)
        return

    if results:
        print("\nTransaction Details:")

        for trans in results:
            print("\nCustomer ID:", trans[0])
            print("Customer Name:", trans[1])
            print("Contact (Email):", trans[2])
            print("Book Ordered:", trans[3])
            print("Price:", trans[4])
            print("Payment Status:", trans[5])

        print("\nEnd of transaction records.")
    main_menu()

def show_sales_report():
    query = "SELECT * FROM CustomerData"
    cursor.execute(query)
    results = cursor.fetchall()
    
    if results:
        total_sales = 0
        print("Customer ID   Customer Name   Email   Book Ordered   Price   Payment Status")
        for row in results:
            print(row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4], " ", row[5])
            total_sales += float(row[4])
        print("\nTotal Sales Amount:", total_sales)
    else:
        print("No records found.")

def delete_book():
    search_choice = input("Search by Book ID or Book Name? (Enter 'ID' or 'Name'): ").strip().lower()
    if search_choice == 'id':
        try:
            book_id = int(input("Enter the Book ID to delete: ").strip())
            query = "SELECT * FROM InventoryManagement WHERE BookID = %s"
            cursor.execute(query, (book_id,))
            result = cursor.fetchone()
        except ValueError:
            print("Invalid input. Please enter a numeric Book ID.")
            return
    elif search_choice == 'name':
        book_name = input("Enter the Book Name to delete: ").strip()
        query = "SELECT * FROM InventoryManagement WHERE LOWER(BookName) LIKE %s"
        cursor.execute(query, ('%' + book_name.lower() + '%',))
        result = cursor.fetchone()
    else:
        print("Invalid choice. Please enter 'ID' or 'Name'.")
        return

    if not result:
        print("No matching book found.")
        return

    print("\nBook found:")
    print("Book ID:", result[0], "Book Name:", result[1], "Market Price:", result[2])
    confirm = input("Is this the correct book? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Deletion process cancelled.")
        return
    reason = input("Please enter the reason for deleting this book: ").strip()

    print("Processing...")
    delete_query = "DELETE FROM InventoryManagement WHERE BookID = %s"
    cursor.execute(delete_query, (result[0],))
    db.commit()
    print("Book deleted successfully.")

    another = input("Do you want to delete another book? (Y/N): ").strip().lower()
    if another == 'y':
        delete_book()  
    else:
        main_menu()
        
def main_menu():
    while True:
        print("\n--- EKR Book Store Management ---")
        print("Welcome")
        print("Choose from 1 to 7 to do various function as per the no. alloted")
        print("1. Add a Book to Inventory")
        print("2. Search for a Book")
        print("3. Show All Books")
        print("4. Add New Order")
        print("5. Show transaction and Payment for Pending Staus")
        print("6. Show Sales Report")
        print("7. Delete book")
        print("Any other key to exit...")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_book_to_inventory()
        elif choice == "2":
            book_name = input("Enter the book name to search: ").strip()
            search_books(book_name)
        elif choice == "3":
            show_all_books()
        elif choice == "4":
            place_order()
        elif choice == "5":
            search_choice = input("Search by Customer ID or Email? (C/E): ").strip().lower()
            if search_choice == 'c':
                customer_id = int(input("Enter the Customer ID: "))
                show_transaction_details(customer_id=customer_id)
            elif search_choice == 'e':
                contact = input("Enter the Email address: ").strip()
                show_transaction_details(contact=contact)
            else:
                print("Invalid choice. Please enter 'C' for Customer ID or 'E' for Email.")
        elif choice =="6":
            show_sales_report()
        elif choice == "7":
            delete_book()
        else :
            print("Invalid Choice.....Exiting the program....")

main_menu()
db.close()
