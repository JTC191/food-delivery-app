from flask import current_app
from . import mysql  # Connects to MySQL Database

from .models import (
    Restaurant,
    Food,
    RestaurantItem,
    Basket,
    Selection,
    DeliveryOption,
    UserInfo,
    UserAccount

)

from uuid import uuid4
from contextlib import closing


# --- Restaurant & Food Queries ---

def get_restaurants():
    try:
        with closing(current_app.mysql.connection.cursor()) as cur:
            cur.execute("SELECT * FROM Restaurant")
            results = cur.fetchall()

        return [
            Restaurant(
                row['restaurantID'],
                row['restaurantName'],
                float(row['averageScore']),
                row['restaurantDescription'],
                row['restaurantImage']
            )
            for row in results
        ]
    except Exception as e:
        current_app.logger.error(f"Error fetching restaurants: {e}")
        return []


def get_food_items():
    try:
        with closing(current_app.mysql.connection.cursor()) as cur:
            cur.execute("SELECT * FROM food")
            rows = cur.fetchall()
        return [Food(**row) for row in rows]
    except Exception as e:
        current_app.logger.error(f"Error fetching food items: {e}")
        return []


def get_food_for_restaurant(restaurant_id):
    try:
        with closing(current_app.mysql.connection.cursor()) as cur:
            cur.execute("""
                SELECT f.*
                FROM food f 
                JOIN restaurantitem ri ON f.foodID = ri.foodID
                WHERE ri.restaurantID = %s
            """, (restaurant_id,))
            rows = cur.fetchall()
        return [Food(**row) for row in rows]
    except Exception as e:
        current_app.logger.error(f"Error fetching food for restaurant {restaurant_id}: {e}")
        return []


# --- Basket & Selection Insertion ---

def insert_basket(basket: Basket):
    try:
        with closing(current_app.mysql.connection.cursor()) as cur:
            cur.execute("""
                INSERT INTO basket (basketID, cardNumber, cvv, deliveryLocation, emailAddress, fullName, deliveryOption)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                basket.basketID, basket.cardNumber, basket.cvv,
                basket.deliveryLocation, basket.emailAddress,
                basket.fullName, basket.deliveryOption.value
            ))
        current_app.mysql.connection.commit()
    except Exception as e:
        current_app.logger.error(f"Error inserting basket: {e}")


def get_selectionIDs():
    cur = mysql.connection.cursor()
    

def check_for_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT user_id, username, user_password, email, firstname, surname, phoneNumber
        FROM user
        WHERE username = %s AND user_password = %s
    """, (username, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(row['username'], row['user_password'], row['email'],
                           UserInfo(str(row['user_id']), row['firstname'], row['surname'],
                                    row['email'], row['phoneNumber']))
    return None  


def is_admin(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM administrators WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    return True if row else False

def insert_selections(foodItem: Food, quantity, basketID:int): #Saves a list of user selections into the database

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO selection (selectionDateTime,basketID,foodID,quantity,foodPrice,foodName)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        "2025-05-24 11:43:09",
        basketID,
        foodItem.foodID,
        quantity,
        foodItem.foodPrice,
        foodItem.foodName
        

    ))
    mysql.connection.commit()
    cur.close()


def update_selection(selectionID:int, quantity:int): #Saves a list of user selections into the database

    cur = mysql.connection.cursor()
    cur.execute("""
        Update selection
        SET quantity = %s
        WHERE selectionID = %s
     """, (
        quantity,
        selectionID,
        
    ))
    mysql.connection.commit()
    cur.close()

def delete_selection(selectionID:int): #Saves a list of user selections into the database
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM selection WHERE selectionID = %s", [selectionID])
    mysql.connection.commit()
    cur.close()

def delete_all_selections(basketID:int): #Saves a list of user selections into the database
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM selection WHERE basketID = %s", [basketID])
    mysql.connection.commit()
    cur.close()


def get_selections_for_basket(basket_id): #Fetches selections for a specific basket from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM selection WHERE basketID = %s", (basket_id,)) #retrieves all rows from selection table where basketID matches one provided
    rows = cur.fetchall()
    cur.close()
    return [Selection(**row) for row in rows] #returns a list of Selection objects

def get_basket(basket_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM basket WHERE basketID = %s", (basket_id,))
    row = cur.fetchone()
    return Basket(**row) if row else None

def get_food_by_id(food_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM food WHERE foodID = %s", (food_id,))
    row = cur.fetchone()
    cur.close()
    return Food(**row) if row else None

def get_restaurant_by_id(restaurant_id):
    try:
        with closing(current_app.mysql.connection.cursor()) as cur:
            cur.execute("SELECT * FROM Restaurant WHERE restaurantID = %s", (restaurant_id,))
            row = cur.fetchone()
        return Restaurant(**row) if row else None
    except Exception as e:
        current_app.logger.error(f"Error fetching restaurant by ID {restaurant_id}: {e}")
        return None

def get_restaurant_by_food_id(food_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT r.restaurantID, r.restaurantName, r.averageScore, r.restaurantDescription, r.restaurantImage
        FROM restaurant r
        JOIN restaurantItem ri ON r.restaurantID = ri.restaurantID
        WHERE ri.foodID = %s
    """, (food_id,))
    
    row = cur.fetchone()
    cur.close()

    if row is None:
        return None

    return Restaurant(**row)

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO user (username, user_password, email, firstname, surname, phoneNumber)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.username.data, form.password.data, form.email.data,
          form.firstname.data, form.surname.data, form.phoneNumber.data))
    mysql.connection.commit()
    cur.close()

def add_food(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO food (foodID, foodPrice, foodName, foodDescription, foodCategory, foodImage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.foodID.data, form.foodPrice.data, form.foodName.data, form.foodDescription.data,
          form.foodCategory.data, form.foodImage.data ))
    mysql.connection.commit()
    cur.close()

def add_restaurant(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO restaurant (restaurantID, restaurantName, averageScore, restaurantDescription, restaurantImage)
        VALUES (%s, %s, %s, %s, %s)
    """, (form.restaurantID.data, form.restarauntName.data, form.restaurantScore.data,
          form.restaurantDescription.data, form.restaurantImage.data))
    mysql.connection.commit()
    cur.close()

def create_basket(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO Basket (user_id)
        VALUES (%s)
    """, (
        user_id
    ))
    mysql.connection.commit()
    cur.close()

def update_checkout(form, basket_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE basket
        SET cardnumber = (%s),
            expiryDate = (%s),
            cvv = (%s),
            deliveryLocation = (%s),
            emailAddress = (%s),
            fullName = (%s),
            deliveryOption = (%s)
            WHERE user_id = (%s);
    """, (form.cardNumber.data, form.expiryDate.data, form.cvv.data,
          form.deliveryLocation.data, form.emailAddress.data, form.fullName.data,
          form.deliveryOption.data, basket_id))
    mysql.connection.commit()
    cur.close()

    
    