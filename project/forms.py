from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, DateField, EmailField, SelectField, DecimalField
from wtforms.validators import InputRequired, email, Length

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField("Username:", validators = [InputRequired()])
    password = PasswordField("Password:", validators = [InputRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    """Form for user registry."""
    username = StringField("Username:", validators = [InputRequired()])
    password = PasswordField("Password:", validators = [InputRequired()])
    email = EmailField("Email:", validators = [InputRequired(), email()])
    firstname = StringField("First Name:", validators = [InputRequired()])
    surname = StringField("Last Name:", validators = [InputRequired()])
    phoneNumber = StringField("Phone number:", validators = [InputRequired()])
    submit = SubmitField("Make Account")

class CheckoutForm(FlaskForm):
    """Form for checkout."""
    cardNumber = StringField("Card Number (16 Numbers):", validators = [InputRequired(), Length(min=16, max=16)])
    expiryDate = DateField("Expiry Date:", validators = [InputRequired()])
    cvv = StringField("CVV (3 Numbers):", validators = [InputRequired(), Length(min=3, max=3)])
    deliveryLocation = StringField("Delivery Location:", validators = [InputRequired()])
    emailAddress = EmailField("Email:", validators = [InputRequired()])
    fullName = StringField("Full Name:", validators = [InputRequired()])
    deliveryOption = SelectField('Delivery Option', choices=[('Standard', 'Standard (No Extra Charge)'), ('Express', 'Express (Extra $5)'), ('Eco-Friendly', 'Eco-Friendly (Extra $10)')])
    submit = SubmitField("Checkout")

class FoodForm(FlaskForm):
    """Form for adding a food item."""
    foodID = StringField("Food ID (format is 'FXXXX' where X is a number):", validators = [InputRequired(), Length(min=5, max=5)])
    foodPrice = DecimalField("Food Price:", validators = [InputRequired()])
    foodName = StringField("Food Name:", validators = [InputRequired()])
    foodDescription = StringField("Description:", validators = [InputRequired()])
    foodCategory = StringField("Category:", validators = [InputRequired()])
    foodImage = StringField("Food Image URL:", validators = [InputRequired()])
    foodSubmit = SubmitField("Add Food Item")

class RestaurantForm(FlaskForm):
    """Form for adding a restaurant."""
    restaurantID = StringField("Restaraunt ID (format is 'RXXXX' where X is a number):", validators = [InputRequired(), Length(min=5, max=5)])
    restarauntName = StringField("Restaraunt Name:", validators = [InputRequired()])
    restaurantScore = DecimalField("Score: ", validators = [InputRequired()])
    restaurantDescription = StringField("Description:", validators = [InputRequired()])
    restaurantImage = StringField("Restaurant Image URL:", validators = [InputRequired()])
    restaurantSubmit = SubmitField("Add Restaurant Item")