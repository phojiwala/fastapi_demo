from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    phone_no = Column(String(15), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Relationship with orders
    orders = relationship("Order", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationship with products: one category can have many products
    products = relationship("Product", back_populates="category")

# Product model
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    flash_sale_price = Column(Float, nullable=True)
    flash_sale_active = Column(Boolean, default=False)

    # Relationship with category: each product belongs to a category
    category = relationship("Category", back_populates="products")
    # Relationship with stock: each product can have a corresponding stock
    stock = relationship("Stock", back_populates="product", uselist=False)
    # Relationship with order items
    order_items = relationship("OrderItem", back_populates="product")

# Stock model
class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)  

    # Relationship with product: each stock corresponds to one product
    product = relationship("Product", back_populates="stock")

# Order model 
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(100), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    discount_percent = Column(Float, default=0.0)  # Store discount percentage
    discount_amount = Column(Float, default=0.0)  # Store the discount amount

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

# OrderItem model (New)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)  # Price * quantity for each item

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

# Payment model (No change)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    payment_status = Column(String(50), default="Pending")  # Payment status: Pending, Successful, Failed

    # Relationships
    order = relationship("Order", back_populates="payment")
