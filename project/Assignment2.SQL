DROP DATABASE IF EXISTS Assignment2;
CREATE DATABASE Assignment2;
USE Assignment2;


-- Create Tables --

-- This table stores relevant data for a particular restaurant

CREATE TABLE User (
    user_id int AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    firstname VARCHAR(100),
    surname VARCHAR(100),
    phoneNumber VARCHAR(20)
);

CREATE TABLE Administrators (
    user_id int key,
    foreign key (user_id) REFERENCES User(user_id)
);

CREATE TABLE Restaurant (
    restaurantID CHAR(5) NOT NULL PRIMARY KEY,
    restaurantName VARCHAR(40) NOT NULL,
    averageScore DECIMAL (3,2),
    restaurantDescription TEXT(255) NOT NULL,
    restaurantImage VARCHAR(100) NOT NULL
);

-- This table stores relevant data for a particular food item

CREATE TABLE Food (
    foodID CHAR(5) NOT NULL PRIMARY KEY,
    foodPrice DECIMAL(10,2) NOT NULL,
    foodName VARCHAR(50) NOT NULL,
    foodDescription TEXT(255) NOT NULL,
    foodCategory VARCHAR(20) NOT NULL,
    foodImage VARCHAR(100) NOT NULL
);

-- Stores all of the food items per restaurant id, so you can look up what
-- restaurant has what food item

CREATE TABLE RestaurantItem(
    restaurantID CHAR(5) NOT NULL,
    foodID CHAR(5) NOT NULL,
    CONSTRAINT PK_RestaurantItem PRIMARY KEY (foodID, restaurantID),
    CONSTRAINT RestaurantItem_Food_FK FOREIGN KEY (foodID) REFERENCES Food(foodID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT RestaurantItem_Restaurant_FK FOREIGN KEY (restaurantID) REFERENCES Restaurant(restaurantID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- This table stores all of the relevant user details for a basket, it
-- does not store what food item is in the basket as that is in the selection
-- table

CREATE TABLE Basket (
    basketID int AUTO_INCREMENT PRIMARY KEY,
    cardNumber CHAR(16),
    expiryDate DATE,
    cvv CHAR(3),
    deliveryLocation VARCHAR(100),
    emailAddress VARCHAR(100),
    fullName VARCHAR(100),
    deliveryOption VARCHAR(50),
    user_id int,
    foreign key (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Each time a food item is added to the basket, the basket ID and food ID is recorded.
-- So when you want to add to a basket, create a new entry in the selection table where:
-- basket ID = the id of the current basket, and foodID is the id of the food item
-- This is used to store all the food items in baskets, so for example if you want to know
-- all of the food items in a basket, you can do SELECT all Food Items WHERE basketID = the basketID you want to know

CREATE TABLE Selection (
    selectionID int AUTO_INCREMENT PRIMARY KEY,
    selectionDateTime DATETIME NOT NULL,
    basketID int NOT NULL,
    foodID CHAR(5) NOT NULL,
    quantity Int(5) NOT NULL,
    foodPrice DECIMAL(10,2),
    foodName VARCHAR(50),
    CONSTRAINT Selection_Basket_FK FOREIGN KEY (basketID) REFERENCES Basket(basketID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT Selection_Food_FK FOREIGN KEY (foodID) REFERENCES Food(foodID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Users
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('admin','8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'gee@mail.com', 'Admin', 'User', '0404123943');
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('admin2','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', 'admin2@mail.com', 'Admin2', 'User2', '0404141234');
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('alekkaroli','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'alek.karoli@gmail.com', 'Aleksander', 'Karoli', '0491886916');
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('testuser2','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'test.user2@gmail.com', 'John', 'Smith', '0414421312');
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('testuser3','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'test.user3@gmail.com', 'Billy', 'Slater', '0418274145');
INSERT INTO User (username, user_password, email, firstname, surname, phoneNumber)
VALUES ('testuser4','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'test.user4@gmail.com', 'Kalyn', 'Ponga', '0941823812');

-- Adding Admins
INSERT INTO Administrators VALUES (1);
INSERT INTO Administrators VALUES (2);

-- Restaurants
INSERT INTO Restaurant VALUES 
('R0001', 'Grill''d', 4.5, 'Grill''d is an Australian-owned burger chain founded in 2004 in Hawthorn, Melbourne.', 'Grill''d_Logo.png'),
('R0002', 'Subway', 4.4, 'Subway IP LLC, trading as Subway, is an American multinational fast food restaurant franchise that specialises in submarine sandwiches (subs) and wraps.', 'Subway_Logo.jpg'),
('R0003', 'Zambrero', 4.6, 'Zambrero is an Australian multinational fast food restaurant franchise serving Mexican cuisine.', 'Zambrero_Logo.png');

-- Foods
INSERT INTO Food VALUES ('F0001', 15.90,     'Best Zing-Ever', 'HFC Pattie, Classic slaw, creamy egg mayo, topped with the certified-zingy Hawthorn Hot Sauce.', 'Burgers', 'Grill''d_HFC_Best_Zing_Ever.png');
INSERT INTO Food VALUES ('F0002', 16.50,     'HFC BLAT', 'RSPCA Approved chicken breast cooked in extra virgin olive oil w/ crispy bacon, cos lettuce, avocado, tomato & herbed mayo', 'Burgers', 'Grill''d_HFC_Blat.jpg');
INSERT INTO Food VALUES ('F0003', 15.90,     'HFC Chipotle', 'RSPCA Approved chicken breast cooked in extra virgin olive oil w/ chipotle mayo, dill pickles, rainbow slaw & Spanish onion', 'Burgers', 'Grill''d_HFC_Chipotle.jpg');
INSERT INTO Food VALUES ('F0004', 14.90,    'HFC Best Classic', 'RSPCA Approved chicken breast cooked in extra virgin olive oil w/ dill pickles, cos lettuce & egg mayo.', 'Burgers', 'Grill''d_HFC_Classic.jpg');
INSERT INTO Food VALUES ('F0005', 13.60,    'Chicken Schnitzel Salad', 'Chicken Schnitzel, Old English Style Cheese, Lettuce, Spinach, Tomato, Cucumber, Capsicum, Onion, Carrot, Olives, Garlic Aioli, Served in a Salad Bowl.', 'Salads & Bowls', 'Subway_Chicken_Schnitzel.png');
INSERT INTO Food VALUES ('F0006', 11.10,     'Turkey Salad', 'Turkey, Natural Cheddar Cheese, Lettuce, Spinach, Tomato, Cucumber, Capsicum, Onion, Carrot, Olives, Honey Mustard, Served in a Salad Bowl.', 'Salads & Bowls', 'Subway_Turkey_Salad.png');
INSERT INTO Food VALUES ('F0007', 13.15,     'Sweet Onion Chicken Teriyaki Salad', 'Chicken Teriyaki, Mozzarella Cheese, Lettuce, Spinach, Tomato, Cucumber, Capsicum, Onion, Carrot, Olives, Sweet Onion Sauce, Served in a Salad Bowl.', 'Salads & Bowls', 'Subway_Sweet_Onion_Chicken_Teriyaki.png');
INSERT INTO Food VALUES ('F0008', 23.40,     'Big Burrito', 'Filling, rice, beans, cheese, sour cream, guacamole, lettuce, Signature Salsa', 'Burritos/Tacos', 'Zambrero_Big_Burrito.jpg');
INSERT INTO Food VALUES ('F0009', 20.90,    'Signature Burrito', 'Filling, black rice, beans, cheese, lettuce, sour cream, salsas, jalapeños & sauce', 'Burritos/Tacos', 'Zambrero_Signature_Burrito.jpg');
INSERT INTO Food VALUES ('F0010', 6.30,     'Soft Taco', 'Filling, cheese, sour cream, lettuce, salsas, jalapeños & sauce on soft shell taco', 'Burritos/Tacos', 'Zambrero_Soft_Taco.jpg');
INSERT INTO Food VALUES ('F0011', 6.90,     'Dos Capas', 'Filling, cheese, sour cream, lettuce, salsas, jalapeños & sauce in a crunch taco shell wrapped in a soft tortilla', 'Burritos/Tacos', 'Zambrero_Dos_Carpas.png');
INSERT INTO Food VALUES ('F0012', 18.90,     'Toasted Burrito', 'Filling, rice, beans, double cheese, sour cream, salsa, jalapeños & sauce', 'Burritos/Tacos', 'Zambrero_Toasted_Burrito.png');
INSERT INTO Food VALUES ('F0013', 14.90,    'Small Burrito', 'Filling, rice, beans, cheese, lettuce, sour cream, salsas, jalapeños & sauce', 'Burritos/Tacos', 'Zambrero_Small_Burrito.png');
INSERT INTO Food VALUES ('F0014', 17.40,     'Small Signature Burrito', 'Filling, black rice, beans, cheese, sour cream, guacamole, lettuce, Signature Salsa, jalapeños & sauce', 'Burritos/Tacos', 'Zambrero_Small_Signature_Burrito.png');
INSERT INTO Food VALUES ('F0015', 18.40,     'Burrito', 'Filling, rice, beans, cheese, lettuce, sour cream, salsas, jalapeños & sauce', 'Burritos/Tacos', 'Zambrero_Burrito.png');

-- Restaurant Items
INSERT INTO RestaurantItem VALUES ('R0001', "F0001");
INSERT INTO RestaurantItem VALUES ('R0001', 'F0002');
INSERT INTO RestaurantItem VALUES ('R0001', 'F0003');
INSERT INTO RestaurantItem VALUES ('R0001', 'F0004');
INSERT INTO RestaurantItem VALUES ('R0002', 'F0005');
INSERT INTO RestaurantItem VALUES ('R0002', 'F0006');
INSERT INTO RestaurantItem VALUES ('R0002', 'F0007');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0008');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0009');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0010');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0011');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0012');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0013');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0014');
INSERT INTO RestaurantItem VALUES ('R0003', 'F0015');


-- Baskets
-- Pre populated baskets
INSERT INTO Basket (cardNumber, expiryDate, cvv, deliveryLocation, emailAddress, fullName, deliveryOption, user_id)
VALUES (0000111122223333, '2025-07-01', 872, "30 Example Street Suburbia 1001", "test.email@gmail.com", "John Smith", "Priority", 1);
INSERT INTO Basket (cardNumber, expiryDate, cvv, deliveryLocation, emailAddress, fullName, deliveryOption, user_id)
VALUES (1111000033332222, '2028-04-05', 674, "60 Example Street Urbanville 1002", "test.email2@gmail.com", "Bryan Abbot", "Standard", 2);
INSERT INTO Basket (cardNumber, expiryDate, cvv, deliveryLocation, emailAddress, fullName, deliveryOption, user_id)
VALUES (3333111100002222, '2029-04-05', 674, "60 Example Street Townton 1004", "test.email4@gmail.com", "Bill Brian", "Eco-Friendly", 3);
-- Unpopulated baskets
INSERT INTO Basket (user_id)
VALUES (4);
INSERT INTO Basket (user_id)
VALUES (5);
INSERT INTO Basket (user_id)
VALUES (6);

-- Selections
-- For Basket 1
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName) 
VALUES ("2022-09-02 10:43:09", 1, "F0001", 1, 15.90,     'Best Zing-Ever');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-09-02 10:47:09", 1, "F0002", 2, 16.50,     'HFC BLAT');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-09-02 10:47:36", 1, "F0003", 3, 15.90,     'HFC Chipotle');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-09-02 10:49:09", 1, "F0005", 4, 13.60,    'Chicken Schnitzel Salad');
-- For Basket 2
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-11-04 10:43:09", 2, "F0001", 1, 15.90,     'Best Zing-Ever');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-11-05 10:47:09", 2, "F0003", 2, 16.50,     'HFC BLAT');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-11-05 10:47:36", 2, "F0004", 3, 15.90,     'HFC Chipotle');
INSERT INTO Selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
VALUES ("2022-11-05 10:49:09", 2, "F0005", 4, 13.60,    'Chicken Schnitzel Salad');