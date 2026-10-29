from seed import seed
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from routes.events import router as events_router
from routes.auth_login import router as auth_router
from routes.auth_register import router as reg_router
from routes.rsvp import router as rsvp_router
from routes.post_events import router as post_events_router

app = FastAPI(title="NC Plus One", debug=True)
app.include_router(events_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(reg_router, prefix="/api") 
app.include_router(rsvp_router, prefix="/api")
app.include_router(post_events_router, prefix="/api")

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

def main():
    seed()

if __name__ == "__main__":
    main()