from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session,joinedload,selectinload
from database import get_db
from models import User, Product, Category, Stock ,Order, OrderItem,Payment
from schemas import *
from utils import hash_password, verify_password, create_access_token,token_required,get_current_user
from typing import List
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        fullname=user_data.fullname,
        username=user_data.username,
        phone_no=user_data.phone_no,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.post("/login")
# def login(user_data: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == user_data.username).first()
#     if not user or not verify_password(user_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": user.username})
#     return {"access_token": token, "token_type": "bearer", "user": user.username}

from sqlalchemy.future import select

@router.post("/login")
async def login(user_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": user.username}

# Category CRUD
@router.post("/categories", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), user_data: User = Depends(token_required)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.put("/categories/{category_id}", response_model=CategoryCreate)
async def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db_category.name = category.name
        print(f"User Data: {user_data.username}, {user_data.email}")
        db.commit()
        db.refresh(db_category)
        return db_category
    raise HTTPException(status_code=404, detail="Category not found")

@router.delete("/categories/{category_id}", response_model=CategoryCreate)
async def delete_category(category_id: int, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return db_category
    raise HTTPException(status_code=404, detail="Category not found")


# Product CRUD
@router.post("/products", response_model=ProductCreate)
async def create_product(product: ProductCreate, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_product = Product(name=product.name, description=product.description, price=product.price, category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Create initial stock for the product
    db_stock = Stock(product_id=db_product.id, quantity=0)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_product

@router.put("/products/{product_id}", response_model=ProductUpdate)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.category_id = product.category_id
        db.commit()
        db.refresh(db_product)
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products/{product_id}", response_model=ProductUpdate)
async def delete_product(product_id: int, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

# @router.get("/list_products", response_model=ProductListResponse)
# async def list_products(db: Session = Depends(get_db), user_data: dict = Depends(token_required)):
#     user_full_name = f"{user_data.fullname}" if user_data else "Guest"
    
#     # Fetch products from database
#     products = db.query(Product).all()
#     product_list = []
#     for product in products:
#         category = db.query(Category).filter(Category.id == product.category_id).first()
#         stock = db.query(Stock).filter(Stock.product_id == product.id).first()
#         product_list.append(ProductResponse(
#             id=product.id,
#             name=product.name,
#             description=product.description,
#             price=product.price,
#             category_id=category.name if category else "Unknown",
#             stock=stock.quantity if stock else 0
#         ))

#     return ProductListResponse(user_full_name=user_full_name, products=product_list)

@router.get("/list_products", response_model=ProductListResponse)
async def list_products(db: AsyncSession = Depends(get_db), user_data: dict = Depends(token_required)):
    user_full_name = f"{user_data.fullname}" if user_data else "Guest"

    # Fetch all products with category and stock using async
    result = await db.stream(
        select(Product)
        .options(
            selectinload(Product.category),  # Efficiently load category
            selectinload(Product.stock)      # Efficiently load stock
        )
    )

    # Process products asynchronously
    product_list = [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category.name if product.category else "Unknown",
            stock=product.stock.quantity if product.stock else 0
        )
        async for product in result.scalars()
    ]

    return ProductListResponse(user_full_name=user_full_name, products=product_list)

# # Stock CRUD
@router.post("/products/{product_id}/stock", response_model=StockResponse)
async def create_stock(product_id: int, stock: StockBase, db: Session = Depends(get_db), user_data: User = Depends(token_required)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Check if there's already an existing stock entry for the product
    db_stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if db_stock:
        # If stock entry exists, increase the quantity
        db_stock.quantity += stock.quantity
        db.commit()
        db.refresh(db_stock)
    else:
        # If no stock entry exists, create a new one
        db_stock = Stock(product_id=product_id, quantity=stock.quantity)
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
    return db_stock


@router.get("/products/{product_id}/stock", response_model=StockTotal)
async def get_stock(product_id: int, db: Session = Depends(get_db), user_data: User = Depends(token_required)):
    total_stock = db.query(func.sum(Stock.quantity)).filter(Stock.product_id == product_id).scalar()
    if total_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return StockTotal(total_quantity=int(total_stock))

@router.put("/products/{product_id}/stock", response_model=StockResponse)
async def update_stock(product_id: int, stock: StockUpdate, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if db_stock:
        db_stock.quantity = stock.quantity
        db.commit()
        db.refresh(db_stock)
        return db_stock
    raise HTTPException(status_code=404, detail="Stock not found")

@router.delete("/products/{product_id}/stock", response_model=StockResponse)
async def delete_stock(product_id: int, db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    db_stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if db_stock:
        db_stock.quantity = 0
        db.commit()
        db.refresh(db_stock)
        return db_stock
    raise HTTPException(status_code=404, detail="Stock not found")

@router.post("/checkout")
async def checkout(data: CheckoutSchema,db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    # Create Order
    order = Order(user_id=user_data.id)
    db.add(order)
    db.commit()
    db.refresh(order)

    total_amount = 0  # Store total price of the order
    total_items = 0  # Count total number of items for discount calculation

    # Add OrderItems (Multiple Products)
    for item in data.products:  # Use validated Pydantic model
        product_id = item.product_id
        quantity = item.quantity

        # Check if the product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        # Check stock availability
        stock = db.query(Stock).filter(Stock.product_id == product_id).first()
        if not stock:
            raise HTTPException(status_code=404, detail=f"No stock information available for product ID {product_id}")
        
        if stock.quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.name}. Available: {stock.quantity}, Requested: {quantity}"
            )
        # Use flash sale price if active, else normal price
        price = product.flash_sale_price if product.flash_sale_active else product.price
        # Calculate total price for this item
        total_price = price * quantity

        # Create OrderItem
        order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity, total_price=total_price)
        db.add(order_item)
        total_amount += total_price  # Add to overall amount
        total_items += quantity  # Increase total items count

        # Update stock quantity
        stock.quantity -= quantity
        db.commit()

    # Apply discount if 3 or more items
    discount_percent = 0
    discount_amount = 0
    if total_items >= 3:
        discount_percent = 5
        discount_amount = total_amount * discount_percent / 100
        total_amount -= discount_amount  # Apply discount
        order.discount_percent = discount_percent
        order.discount_amount = discount_amount
        db.commit()

    # Create Payment entry
    payment = Payment(order_id=order.id, amount=total_amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "order_id": order.id,
        "payment_id": payment.id,
        "status": "Order placed successfully",
        "total_amount": total_amount,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount
    }

# 2. Update Payment Status API (No change)
@router.put("/update_payment_status/{payment_id}")
async def update_payment_status(payment_id: int,update_data: PaymentStatusUpdate,db: Session = Depends(get_db),user_data: User = Depends(token_required)):
    if update_data.payment_status not in ["Pending", "Successful", "Failed"]:
        raise HTTPException(status_code=400, detail="Invalid payment status")

    # Fetch Payment entry
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Update payment status
    payment.payment_status = update_data.payment_status
    db.commit()
    db.refresh(payment)

    # Update order status based on payment status
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if update_data.payment_status == "Successful":
        order.status = "Completed"
    elif update_data.payment_status == "Failed":
        order.status = "Cancelled"
    
    db.commit()

    return {
        "order_id": order.id,
        "payment_status": payment.payment_status,
        "order_status": order.status
    }

@router.get("/my_orders", response_model=list[OrderResponse])
def get_user_orders(db: Session = Depends(get_db), user_data: User = Depends(token_required)):
    user_id = user_data.id
    # Fetch orders and related items in one query
    orders = db.query(Order).options(joinedload(Order.order_items)).filter(Order.user_id == user_id).all()
    if not orders:
        return []
    
    # Convert to Pydantic-compatible response
    return [
        OrderResponse(
            order_id=order.id,
            status=order.status,
            total_price=sum(item.total_price for item in order.order_items),  
            discount_percent=order.discount_percent,
            discount_amount=order.discount_amount,
            final_price=sum(item.total_price for item in order.order_items) - order.discount_amount,
            created_at=order.created_at,
            items=[
                OrderItemResponse(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    total_price=item.total_price
                ) for item in order.order_items
            ]
        )
        for order in orders
    ]
