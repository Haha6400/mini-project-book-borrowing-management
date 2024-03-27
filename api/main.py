from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import records
from routers import books
from routers import borrowers

router = FastAPI()


origins = ["http://localhost:3000"] 
router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/")
def root_access():
    return {"message": "Hello World"}

router.include_router(records.router, tags = ["Records"])
router.include_router(books.router,  tags = ["Books"])
router.include_router(borrowers.router, tags = ["Borrowers"])
