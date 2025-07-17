Make sure to install the required libraries using the requirements.txt file
Run the following commands before attempting to run this code.
For mac users, we need to do some setup before the pip install will work,
so we have made a seperate bash script to run instead. 

### Windows
```bash
py -m pip install -r requirements.txt
```

### MacOS
You may need to find where mysqlserver has been installed for the following
script to set some flags.
To find if where it may be installed at execute the following command on
the terminal:
```bash
sudo find /usr -name mysql.h
```
Then, using what is found, we may need to update the variable named 
`mysqlhome` if it differs with our default.

```bash
chmod +x ./mac.sh && sudo ./mac.sh
```

# Database setup

Execute the Assignment2.SQL file. Assignment2.SQL creates the database Assignment2 and populates it

Make sure that app.config['MYSQL_PASSWORD'] = 'root' is true for your system

# Database structure

Food table stores all food items and relevant data for each

Restaurant table stores all restaurants and relevant data for each

RestaurantItem table facilitates relationship between food items and restaurants. Can be used to look up what food item is at what store

User table stores all users and relevant data for each

Admin table facilitates the assigning of users to admin role, if a user is in the admin table, then they get admin privileges

Basket table stores data about each user's basket. A basket is generated for the user on account creation. Each user has a unique basket

Selection table stores each individual order and relates it to a basket. When a selection is added to cart, the information relating to the food
item (quantity, price etc) is stored and assigned to the basket id of the currently logged in user. 


# User Accounts

There are two admin accounts with the following details:

```
username: admin
password: admin

```
username: admin2
password: root

```

There are 4 basic users with no admin priveleges:

```
username: alekkaroli
password: password

```
username: testuser2
password: password

```
username: testuser3
password: password

```
username: testuser4
password: password

```

# The users: admin, admin2, and alekkaroli have prepopulated baskets. The rest of the users have initialised baskets that are not populated with data