from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from database import SessionLocal
from models import Product

# Define timezone (change as needed)
TIMEZONE = pytz.timezone("UTC")  # Change this to your timezone

def activate_flash_sales():
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.flash_sale_price != None).all()
        for product in products:
            product.flash_sale_active = True  # Enable flash sale
        db.commit()
        print("Flash sale activated!")
    finally:
        db.close()

def deactivate_flash_sales():
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.flash_sale_active == True).all()
        for product in products:
            product.flash_sale_active = False  # Disable flash sale
        db.commit()
        print("Flash sale deactivated!")
    finally:
        db.close()

# Initialize Scheduler
print("Starting scheduler...")
scheduler = BackgroundScheduler()
scheduler.add_job(activate_flash_sales, "cron", day_of_week="fri", hour=18, timezone=TIMEZONE)
scheduler.add_job(deactivate_flash_sales, "cron", day_of_week="fri", hour=22, timezone=TIMEZONE)
scheduler.start()
