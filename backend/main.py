from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import efectores, zonas

app = FastAPI()

# CORS habilitado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(efectores.router)
app.include_router(zonas.router)
