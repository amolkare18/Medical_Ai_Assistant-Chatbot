from fastapi import FastAPI
app = FastAPI()
from middlewares.exception_handlers import catch_exceptions_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router
from routes.upload_pdfs import router as root2
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### exception handlers

app.middleware("http")(catch_exceptions_middleware)


###routers
@app.get("/")
async def root2():
    return {"message": "This is a test2 endpoint"}
app.include_router(upload_router)
app.include_router(ask_router)

