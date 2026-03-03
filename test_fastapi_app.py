from fastapi import FastAPI
from pulsecheck.fastapi import make_health_router
from pulsecheck.core import HealthRegistry

app = FastAPI()

registry = HealthRegistry(environment="local")

app.include_router(make_health_router(registry))

@app.get("/")
def root():
    return {"ok": True}
