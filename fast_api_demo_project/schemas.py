from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    fullname: str
    username: str
    phone_no: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    fullname: str
    username: str
    phone_no: str
    email: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):  # ✅ This will be used in the response
    id: int
    name: str

    class Config:
        from_attributes = True 

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: str
    stock: Optional[int] = 0  # Default to 0 if no stock record

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    user_full_name: str
    products: List[ProductResponse]

class StockBase(BaseModel):
    quantity: int

class StockUpdate(BaseModel):
    quantity: int

class StockTotal(BaseModel):
    total_quantity: int
    
class StockResponse(BaseModel):
    id: int
    quantity: int
    product_id: int

    class Config:
        from_attributes = True
        

# Define a Pydantic model for order items
class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

# Define Pydantic model for checkout request
class CheckoutSchema(BaseModel):
    products: List[OrderItemSchema]
    
class PaymentStatusUpdate(BaseModel):
    payment_status: str

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    total_price: float

    class Config:
        from_attributes = True  # Ensures SQLAlchemy compatibility

class OrderResponse(BaseModel):
    order_id: int
    status: str
    total_price: float
    discount_percent: float
    discount_amount: float
    final_price: float
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True