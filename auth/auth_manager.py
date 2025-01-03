from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from utils.ssh_client import SSHClient
from typing import Optional
import secrets

class AuthManager:
    def __init__(self):
        self.security = HTTPBasic()
        self._sessions = {}  
        self.ssh_client = SSHClient()

    def get_login_page(self) -> str:
        """Returns the login page HTML."""
        return """
        <html>
            <head>
                <title>Node Management Login</title>
                <style>
                    .login-container {
                        max-width: 400px;
                        margin: 50px auto;
                        padding: 20px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    .form-group label {
                        display: block;
                        margin-bottom: 5px;
                    }
                    .form-group input {
                        width: 100%;
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .submit-btn {
                        background-color: #007bff;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .submit-btn:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="login-container">
                    <h1 style="text-align: center;">Login to Node Management System</h1>
                    <form action="/login" method="post">
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <div style="text-align: center;">
                            <button type="submit" class="submit-btn">Login</button>
                        </div>
                    </form>
                </div>
            </body>
        </html>
        """

    async def login(self, username: str = Form(...), password: str = Form(...)):
        """Handle login attempts and create session if successful."""
        if self.validate_credentials(username, password):
            session_token = secrets.token_urlsafe(32)
            self._sessions[session_token] = {"username": username, "password": password}
            response = RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie(key="session", value=session_token, httponly=True)
            return response
        
        return HTMLResponse(
            content=self.get_login_error_page(),
            status_code=401
        )

    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate credentials using SSH connection."""
        return self.ssh_client.test_connection(username, password)

    def get_current_user(self, session: Optional[str] = None) -> Optional[dict]:
        """Get current user from session."""
        if session and session in self._sessions:
            return self._sessions[session]
        return None

    def get_login_error_page(self) -> str:
        """Returns the login error page HTML."""
        return """
        <html>
            <head>
                <title>Login Failed</title>
                <style>
                    .error-container {
                        max-width: 400px;
                        margin: 50px auto;
                        padding: 20px;
                        border: 1px solid #ff4444;
                        border-radius: 5px;
                        background-color: #ffebee;
                        text-align: center;
                    }
                    .back-link {
                        color: #007bff;
                        text-decoration: none;
                    }
                    .back-link:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>Login Failed</h1>
                    <p>Invalid username or password.</p>
                    <p><a href="/" class="back-link">Back to Login</a></p>
                </div>
            </body>
        </html>
        """