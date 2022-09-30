import sqlite3

conn = sqlite3.connect('vending_machine.db')

cursor = conn.cursor()


cursor.executescript(
    '''
    CREATE TABLE Vending_Machine 
    (id     INT     NOT NULL,
    PRIMARY KEY(id));

    CREATE TABLE Candy 
    (vm_id              INT             NOT NULL,
    candy_id            INT             NOT NULL,
    name                VARCHAR(50)     NOT NULL,
    type                VARCHAR(50)     NOT NULL,
    wrapper_color       VARCHAR(50)     NOT NULL,
    price               DOUBLE          NOT NULL,
    quantity            INT             NOT NULL,
    trashed_quantity    INT             NOT NULL,
    FOREIGN KEY(vm_id) REFERENCES Vending_Machine(id),
    PRIMARY KEY(candy_id));

    INSERT INTO Candy (vm_id, candy_id, name, type, wrapper_color, price, quantity, trashed_quantity)
    VALUES (1, 1, 'Sour Skittles', 'Sour', 'Green', 3, 23, 0 );

    INSERT INTO Candy (vm_id, candy_id, name, type, wrapper_color, price, quantity, trashed_quantity)
    VALUES (1, 2, 'Skittles', 'Sweet', 'Red', 2.5, 35, 0 );

    INSERT INTO Candy (vm_id, candy_id, name, type, wrapper_color, price, quantity, trashed_quantity)
    VALUES (1, 3, 'Skittles Sweet Heat', 'Spicy', 'Black', 3, 13, 0 );

    INSERT INTO Candy (vm_id, candy_id, name, type, wrapper_color, price, quantity, trashed_quantity)
    VALUES (1, 4, 'Reeses Peanut Butter Cups', 'Salty', 'Orange', 4, 44, 0 );

    INSERT INTO Vending_Machine (id) 
    VALUES (1 );
    '''
)

conn.commit()
conn.close()