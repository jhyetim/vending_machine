import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Vending_Machine INNER JOIN Candy ON Vending_Machine.id = Candy.vm_id;")
    rows = cur.fetchall()

    print("\n----------------------- Vending Machine ----------------------")
    print("%-4s %-28s %-9s %s %12s" % ("ID", "Name", "Type", "Price", "Quantity"))
    print("--------------------------------------------------------------")
    for i in range(0, len(rows)):
        print("%-4d %-28s %-9s %.2f %7d" % (rows[i][2], rows[i][3], rows[i][4], rows[i][6], rows[i][7]))
    print()

def vending_machine(conn, run, reciept):
    # Get user input
    val = input("How much do you want to put in: ")
    try:
        int(val)
    except ValueError:
        try:
            float(val)
        except ValueError:
            print("PLEASE ENTER A VALID NUMBER")
            run = False

    while run:
        select_all_tasks(conn)
        buy_item = input("Enter the item id of the product you want to buy: ")
        try:
            int(buy_item)
        except ValueError:
            print("PLEASE ENTER A VALID ITEM ID")
            break

        # Get the list of candy id
        cur = conn.cursor()
        cur.execute("SELECT candy_id FROM Candy;")
        rows = cur.fetchall()
        item_id = []
        for i in range(0, len(rows)):
            item_id.append(rows[i][0])

        # Get the cost of the item
        cur.execute("SELECT price FROM Candy WHERE candy_id = {};".format(int(buy_item)))
        rows = cur.fetchall()
        price = rows[0][0]

        if int(buy_item) not in item_id:
            print("THE PRODUCT ID DOES NOT EXIST")
        else:
            # If the price of the item is less than how much the user entered
            if (float(val) > price):
                # Add the item to the reciept
                reciept.append(int(buy_item))

                # Update the quantity
                cur.execute("UPDATE Candy SET quantity = quantity - 1 WHERE candy_id = {} and quantity > 0;".format(int(buy_item)))
                conn.commit

                # Update the trashed_quantity
                cur.execute("UPDATE Candy SET trashed_quantity = trashed_quantity + 1 WHERE candy_id = {};".format(int(buy_item)))
                conn.commit

                # Update the val
                val = float(val) - price
                print("You have $%.2f remaining" % val)
            else:
                print("INSUFFICIENT FUNDS - You have ${} remaining".format(val))

        # Ask the user if they want to continue adding more items
        add_item = str(input("Enter q to quit or any other key to add more items: "))
        if add_item == "q":
            print("Your remaining change is $%.2f" % val)
            run = False

def create_reciept(conn, reciept):
    cur = conn.cursor()
    total = 0

    print("\n----------- Reciept -----------")

    for i in range(0, len(reciept)):
        cur.execute("SELECT name FROM Candy WHERE candy_id = {};".format(reciept[i]))
        rows = cur.fetchall()
        name = rows[0][0]
        cur.execute("SELECT price FROM Candy WHERE candy_id = {};".format(reciept[i]))
        rows = cur.fetchall()
        price = rows[0][0]
        total = total + price
        print("%-25s $%.2f" % (name, price))
    
    print("%-25s $%.2f" % ("Total", total))

def popular_candy(conn):
    cur = conn.cursor()

    cur.execute("SELECT MAX(trashed_quantity) FROM Candy")
    rows = cur.fetchall()
    maxNum = rows[0][0]

    cur.execute("SELECT name FROM Candy WHERE trashed_quantity == {}".format(maxNum))
    rows = cur.fetchall()
    maxName = rows[0][0]

    cur.execute("SELECT wrapper_color FROM Candy WHERE trashed_quantity == {}".format(maxNum))
    rows = cur.fetchall()
    wrapperColor = rows[0][0]

    print("\nThe more popular candy is {} with {} {} wrappers in the trash compartment".format(maxName, maxNum, wrapperColor))

def main():
    run = True
    reciept = []

    conn = create_connection("vending_machine.db")
    vending_machine(conn, run, reciept)
    if (len(reciept) > 0):
        create_reciept(conn, reciept)
        popular_candy(conn)
    
    conn.close()

if __name__ == '__main__':
    main()
