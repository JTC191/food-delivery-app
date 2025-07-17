from flask import Blueprint, render_template, request, session, flash
from flask import redirect, url_for

from hashlib import sha256
from . import mysql
from project.db import *
from .db import get_food_by_id, get_restaurant_by_food_id, add_user, create_basket, update_checkout
from project.forms import LoginForm, RegisterForm, CheckoutForm, FoodForm, RestaurantForm


bp = Blueprint('main', __name__)



# Define the route for the home page (index)
@bp.route('/')
def index():
    category = request.args.get('category')

    all_foods = get_food_items()

    if category == 'Burgers':
        foods = [food for food in all_foods if food.foodID in ['F0001', 'F0002', 'F0003', 'F0004']]
    elif category == 'Burritos':
        foods = [food for food in all_foods if food.foodID in ['F0008', 'F0009', 'F0010', 'F0011', 'F0012', 'F0013', 'F0014', 'F0015']]
    elif category == 'Salads & Bowls':
        foods = [food for food in all_foods if food.foodID in ['F0005', 'F0006', 'F0007']]
    else:
        foods = all_foods

    # Get associated restaurants via join table
    restaurant_objs = []
    seen_ids = set()
    for food in foods:
        restaurant = get_restaurant_by_food_id(food.foodID)
        if restaurant and restaurant.restaurantID not in seen_ids:
            restaurant_objs.append(restaurant)
            seen_ids.add(restaurant.restaurantID)

    return render_template('index.html', foods=foods, restaurants=restaurant_objs)


# Database test function
@bp.route("/test-db")
def test_db():
    return get_food_items()

# Define the route for the About/Product Details page
@bp.route('/about/<food_id>')
def about(food_id):
    food = get_food_by_id(food_id)
    if not food:
        return render_template('404.html', message=f"Food item with ID '{food_id}' not found."), 200

    restaurant = get_restaurant_by_food_id(food_id)
    
    # DEBUG: check what you’re passing
    print("RESTAURANT:", restaurant)
    
    return render_template('product_details.html', food=food, restaurant=restaurant)

@bp.post('/basket/add/<food_id>') 
def adding_to_basket(food_id): # adds to selection
    quantity = request.form.get('quantity')
    basket_id = session['user']['user_id']
    foodItem = get_food_by_id(food_id)
    insert_selections(foodItem, quantity, basket_id)
    return redirect(request.referrer or url_for('main.index'))

@bp.post('/basket/update/<selection_id>') 
def updating_basket(selection_id): # adds to selection
    quantity = request.form.get('quantity')
    update_selection(selection_id,quantity)
    return redirect(url_for('main.deliveryRequest'))  # Goes to checkout page


@bp.post('/basket/delete/<selection_id>') 
def deleting_from_basket(selection_id): # adds to selection
    delete_selection(selection_id)
    return redirect(url_for('main.deliveryRequest'))  # Goes to checkout page
    
@bp.post('/basket/deleteall/') 
def deleting_all(): # adds to selection
    basket_id = session['user']['user_id']
    delete_all_selections(basket_id)
    return redirect(url_for('main.deliveryRequest'))  # Goes to checkout page

@bp.route('/delivery/')
def deliveryRequest():
    basket_id = session['user']['user_id']
    #selections = get_selections_for_basket(basket_id)

    # For each selection, add food details (price, name) from Food table
    #for selection in selections:
    #    food = get_food_by_id(selection.foodID)
    #    if food:
     #     selection.foodPrice = food.foodPrice
     #     selection.foodName = food.foodName

    #return render_template('delivery_request.html', basket=selections)
    return render_template('delivery_request.html', basket=get_selections_for_basket(basket_id))  # Displays Checkout Page'

# Define the route for the Checkout Page 
#@bp.route('/checkoutPage')
#def checkoutPage():
#    basket_id = session['user']['user_id']
#    currentBasket = get_basket(basket_id)
#   return render_template('checkout.html', basket=get_selections_for_basket(basket_id))  # Displays Checkout Page'

@bp.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            user = check_for_user(form.username.data, form.password.data)
            if not user:
                flash('Invalid username or password', 'error')
                return redirect(url_for('main.login'))

            # Store full user info in session
            session['user'] = {
                'user_id': user.info.id,
                'firstname': user.info.firstname,
                'surname': user.info.surname,
                'email': user.info.email,
                'phoneNumber': user.info.phoneNumber,
                'is_admin': is_admin(user.info.id),
            }
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('main.index'))

    return render_template('login.html', form=form)
@bp.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@bp.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.password.data = sha256(form.password.data.encode()).hexdigest()
            # Check if the user already exists
            user = check_for_user(form.username.data, form.password.data)
            if user:
                flash('User already exists', 'error')
                return redirect(url_for('main.register'))

            add_user(form)
            flash('Registration successful!')
            user = check_for_user(form.username.data, form.password.data)
             # Store full user info in session
            session['user'] = {
                'user_id': user.info.id,
                'firstname': user.info.firstname,
                'surname': user.info.surname,
                'email': user.info.email,
                'phoneNumber': user.info.phoneNumber,
                'is_admin': is_admin(user.info.id),
            }
            session['logged_in'] = True
            create_basket(user.info.id)
            return redirect(url_for('main.index'))

    return render_template('register.html', form=form)

@bp.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    basket_id = session['user']['user_id']
    if not get_selections_for_basket(basket_id):
            flash('Basket Empty!')
            return redirect(url_for('main.deliveryRequest'))
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                update_checkout(form, basket_id)
                flash('Checkout successful!')
                return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
    return render_template('checkout.html', basket=get_selections_for_basket(basket_id), form=form)  # Displays Checkout Page'

@bp.route('/manage/', methods=['POST', 'GET'])
# @only_admins
def manage():
    foodForm = FoodForm()
    restaurantForm = RestaurantForm()
    # check if the user is logged in and is an admin
    if 'user' not in session or session['user']['user_id'] == 0:
        flash('Please log in before managing orders.', 'error')
        return redirect(url_for('main.login'))
    if not session['user']['is_admin']:
        flash('You do not have permission to manage orders.', 'error')
        return redirect(url_for('main.index'))
    try:
        if foodForm.validate_on_submit():
            # Add the new city to the database
            add_food(foodForm)
            flash('Food added successfully!')
        elif restaurantForm.validate_on_submit():
            # Add the new tour to the database
            add_restaurant(restaurantForm)
            flash('Restaurant added successfully!')
        else:
            flash('Failed to add food item or restaurant. Please check your input.')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
    
    
    return render_template('manage.html', foodForm=foodForm, restaurantForm=restaurantForm)
