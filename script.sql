CREATE DATABASE hotel_automation;

USE hotel_automation;

-- Table: Guest
CREATE TABLE Guest (
    guestID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(15),
    email VARCHAR(100),
    password VARCHAR(100),
    isFrequentGuest BOOLEAN DEFAULT FALSE
);

-- Table: Receptionist
CREATE TABLE Receptionist (
    receptionistID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(100),
    password VARCHAR(100)
);

-- Table: Room
CREATE TABLE Room (
    roomNumber INT PRIMARY KEY,
    type ENUM('Single', 'Double'),
    isAC BOOLEAN,
    baseTariff FLOAT,
    currentTariff FLOAT,
    isOccupied BOOLEAN DEFAULT FALSE
);

-- Table: Reservation
CREATE TABLE Reservation (
    reservationID INT AUTO_INCREMENT PRIMARY KEY,
    guestID INT,
    roomNumber INT,
    checkInDate DATE,
    checkOutDate DATE,
    advancePaid FLOAT,
    FOREIGN KEY (guestID) REFERENCES Guest(guestID),
    FOREIGN KEY (roomNumber) REFERENCES Room(roomNumber)
);

-- Table: Token
CREATE TABLE Token (
    tokenID INT AUTO_INCREMENT PRIMARY KEY,
    guestID INT,
    issuedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guestID) REFERENCES Guest(guestID)
);

-- Table: FoodItem
CREATE TABLE FoodItem (
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(100),
    pricePerUnit FLOAT
);

-- Table: CateringOrder
CREATE TABLE CateringOrder (
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    guestID INT,
    dateTime DATETIME,
    FOREIGN KEY (guestID) REFERENCES Guest(guestID)
);

-- Table: OrderItems (many-to-many for CateringOrder and FoodItem)
CREATE TABLE OrderItems (
    orderID INT,
    itemID INT,
    quantity INT,
    PRIMARY KEY(orderID, itemID),
    FOREIGN KEY (orderID) REFERENCES CateringOrder(orderID),
    FOREIGN KEY (itemID) REFERENCES FoodItem(itemID)
);

-- Table: Bill
CREATE TABLE Bill (
    billID INT AUTO_INCREMENT PRIMARY KEY,
    guestID INT,
    totalAmount FLOAT,
    isPaid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (guestID) REFERENCES Guest(guestID)
);
