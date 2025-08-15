from dataclasses import dataclass, field
from typing import List
from enum import Enum
from uuid import uuid4 #makes a random unique ID (e.g., for basket)#


# Delivery options: matches the DeliveryOption enum in the database
class DeliveryOption(Enum):
    STANDARD = "Standard"
    EXPRESS = "Express"
    ECOFRIENDLY = "Eco-friendly"

# Restaurant: corresponds to the Restaurant table
@dataclass
class Restaurant:
    restaurantID: str
    restaurantName: str
    averageScore: float
    restaurantDescription: str
    restaurantImage: str
    
# Food item: corresponds to the Food table
@dataclass
class Food:
    foodID: str
    foodName: str
    foodDescription: str
    foodPrice: float
    foodCategory: str
    foodImage: str

# RestaurantItem: links a food to a restaurant (join table)
@dataclass
class RestaurantItem:
    restaurantID: str
    foodID: str

# Selection: a row in the Selection table — a user picks a food for their basket
@dataclass
class Selection:
    selectionID: str = field(default_factory=lambda: str(uuid4())[:8])
    basketID: str = ''
    foodID: str = ''
    selectionDateTime: str = ''
    quantity: int = 1
    foodName: str = ''         # Optional: for displaying in UI
    foodPrice: float = 0.0     # Optional: for calculating total

    def total_price(self):
        return self.foodPrice * self.quantity

# Basket: matches the Basket table (includes user details & delivery info)
@dataclass
class Basket:
    basketID: str = field(default_factory=lambda: str(uuid4())[:8])
    user_id: int = 0
    expiryDate: str = ''
    cardNumber: str = ''
    cvv: str = ''
    deliveryLocation: str = ''
    emailAddress: str = ''
    fullName: str = ''
    deliveryOption: DeliveryOption = DeliveryOption.STANDARD
    selections: List[Selection] = field(default_factory=lambda: [])  # all food items in the basket

    def add_selection(self, selection: Selection):
        self.selections.append(selection)

    def remove_selection(self, selectionID: str):
        self.selections = [s for s in self.selections if s.selectionID != selectionID]

    def get_selection(self, selectionID: str):
        for s in self.selections:
            if s.selectionID == selectionID:
                return s
        return None

    def total_cost(self):
        return sum(selection.total_price() for selection in self.selections)

    def empty(self):
        self.selections = []

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phoneNumber: str

@dataclass
class UserAccount:
    username: str
    password: str
    email: str
    info: UserInfo