from fastapi import FastAPI
from api import router as api_router
from database import Base, engine
from scheduler import scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add root redirect to login
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

# Route to serve the Register page
@app.get("/register", response_class=HTMLResponse)
async def read_register():
    with open("templates/register.html", "r") as file:
        return file.read()

# Route to serve the Login page
@app.get("/login", response_class=HTMLResponse)
async def read_login():
    with open("templates/login.html", "r") as file:
        return file.read()

@app.get("/products", response_class=HTMLResponse)
async def read_products():
    with open("templates/products.html", "r") as file:
        return file.read()

@app.get("/products2", response_class=HTMLResponse)
async def read_products():
    with open("templates/products2.html", "r") as file:
        return file.read()

# Create tables if not exists
# Base.metadata.create_all(bind=engine)
# Include API routes
app.include_router(api_router)

# Run the scheduler when the app starts
if not scheduler.running:
    scheduler.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


