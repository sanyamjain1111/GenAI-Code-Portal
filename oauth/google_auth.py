from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__)
oauth = OAuth() 

def init_oauth(app):
    """Initialize OAuth with Flask app"""
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        userinfo_endpoint="https://openidconnect.googleapis.com/v3/userinfo", 
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={"scope": "openid email profile"},
    )

@auth_bp.route("/login")
def login():
    google = oauth.create_client("google")
    return google.authorize_redirect(url_for("auth.callback", _external=True))

@auth_bp.route("/auth/callback")
def callback():
    google = oauth.create_client("google") 
    token = google.authorize_access_token()
    
    print("\n🔍 OAuth Token Response:", token, "\n")

    if "access_token" not in token:
        return "OAuth failed: No access token received.", 400
    
    user_info = {
        "email": token.get("userinfo", {}).get("email"),
        "name": token.get("userinfo", {}).get("name"),
        "picture": token.get("userinfo", {}).get("picture"),
    }

    print("\n👤 User Info Response:", user_info, "\n")

    session["user"] = user_info 
    return redirect(url_for("dashboard"))