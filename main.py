from fastapi import FastAPI, Depends, Cookie, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from visualization.dashboard import Dashboard
from auth.auth_manager import AuthManager
from typing import Optional
import uvicorn

# Create the FastAPI app instance
app = FastAPI()
auth_manager = AuthManager()
dashboard = Dashboard()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return auth_manager.get_login_page()

@app.post("/login")
async def login(response=Depends(auth_manager.login)):
    return response

# Initialize dashboard with credentials once
dash_initialized = False

@app.get("/dashboard")
async def get_dashboard(session: Optional[str] = Cookie(None)):
    global dash_initialized
    user = auth_manager.get_current_user(session)
    
    if not user:
        return RedirectResponse(url="/")
    
    if not dash_initialized:
        dashboard.initialize_with_credentials(user["username"], user["password"])
        app.mount("/dashboard", WSGIMiddleware(dashboard.app.server))
        dash_initialized = True
    
    return RedirectResponse(url="/dashboard/")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
