# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# Define the declarative Base
Base = declarative_base()

# Table Definitions

class Customer(Base):
    """
    description: A table to store customer information. Each customer has a balance and a credit limit.
    """
    __tablename__ = 'customers'

    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    credit_limit = Column(Float, nullable=False, default=0)
    balance = Column(Float, nullable=False, default=0)

    orders = relationship("Order", back_populates="customer")

class Order(Base):
    """
    description: A table to store order information. Each order is linked to a customer and contains multiple items.
    """
    __tablename__ = 'orders'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    amount_total = Column(Float, nullable=False, default=0)
    notes = Column(String)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """
    description: A table to store items in an order. Each item is linked to a product.
    """
    __tablename__ = 'order_items'

    id = Column(Integer, Sequence('order_item_id_seq'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False, default=0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Product(Base):
    """
    description: A table to store product information.
    """
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0)

# Additional Tables for 12 total requirement

class Address(Base):
    """
    description: A table to store customer addresses.
    """
    __tablename__ = 'addresses'

    id = Column(Integer, Sequence('address_id_seq'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

class Supplier(Base):
    """
    description: A table to store supplier information.
    """
    __tablename__ = 'suppliers'

    id = Column(Integer, Sequence('supplier_id_seq'), primary_key=True)
    name = Column(String, nullable=False)

class Inventory(Base):
    """
    description: A table to track product inventory levels.
    """
    __tablename__ = 'inventory'

    id = Column(Integer, Sequence('inventory_id_seq'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

class Shipment(Base):
    """
    description: A table to store shipment information for orders.
    """
    __tablename__ = 'shipments'

    id = Column(Integer, Sequence('shipment_id_seq'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    shipment_date = Column(DateTime, default=datetime.now)

class Payment(Base):
    """
    description: A table to store payment details for orders.
    """
    __tablename__ = 'payments'

    id = Column(Integer, Sequence('payment_id_seq'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)

class Promotion(Base):
    """
    description: A table for storing promotions applicable to products.
    """
    __tablename__ = 'promotions'

    id = Column(Integer, Sequence('promotion_id_seq'), primary_key=True)
    description = Column(String, nullable=False)
    discount = Column(Float, nullable=False)

class Category(Base):
    """
    description: A table to categorize products for better organization.
    """
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String, nullable=False)

class Employee(Base):
    """
    description: A table to store information about employees.
    """
    __tablename__ = 'employees'

    id = Column(Integer, Sequence('employee_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)

# Database Configuration
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Sample Data Insertion

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample Data
customers = [
    Customer(name="Acme Corporation", credit_limit=5000, balance=3500),
    Customer(name="Globex Corporation", credit_limit=3000, balance=1500),
    Customer(name="Initech Inc", credit_limit=4000, balance=1000),
]

products = [
    Product(name="Widget", price=25),
    Product(name="Gadget", price=30),
    Product(name="Doodad", price=15),
]

# Insert Customers and Products
session.add_all(customers + products)
session.commit()

orders = [
    Order(customer_id=1, amount_total=50, notes="First order"),
    Order(customer_id=2, amount_total=75, notes="Second order"),
    Order(customer_id=3, amount_total=100, notes="Third order"),
]

# Insert Orders
session.add_all(orders)
session.commit()

order_items = [
    OrderItem(order_id=1, product_id=1, quantity=2, unit_price=25, total_price=50),
    OrderItem(order_id=2, product_id=2, quantity=3, unit_price=25, total_price=75),
    OrderItem(order_id=3, product_id=3, quantity=4, unit_price=25, total_price=100),
]

# Insert Order Items
session.add_all(order_items)
session.commit()

addresses = [
    Address(customer_id=1, street="123 Elm Street", city="Springfield", postal_code="12345"),
    Address(customer_id=2, street="456 Maple Avenue", city="Greendale", postal_code="23456"),
]

suppliers = [
    Supplier(name="Supplier One"),
    Supplier(name="Supplier Two"),
]

inventory = [
    Inventory(product_id=1, quantity=100),
    Inventory(product_id=2, quantity=150),
    Inventory(product_id=3, quantity=200),
]

shipments = [
    Shipment(order_id=1, shipment_date=datetime(2023, 1, 1)),
    Shipment(order_id=2, shipment_date=datetime(2023, 2, 1)),
]

payments = [
    Payment(order_id=1, amount_paid=50),
    Payment(order_id=2, amount_paid=75),
]

promotions = [
    Promotion(description="Summer Sale", discount=10),
    Promotion(description="Winter Sale", discount=15),
]

categories = [
    Category(name="Electronics"),
    Category(name="Furniture"),
]

employees = [
    Employee(name="John Doe", position="Manager"),
    Employee(name="Jane Smith", position="Sales"),
]

# Insert all additional data
session.add_all(addresses + suppliers + inventory + shipments + payments +
                promotions + categories + employees)
session.commit()

# Close the session
session.close()
