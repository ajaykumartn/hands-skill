import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os

def initialize_firebase():
    try:
        # Fetch the Firebase service account path from an environment variable
        firebase_cert_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/DELL/Downloads/hands-skill-firebase-adminsdk-fbsvc-bfbd4ceba0.json"


        if not firebase_cert_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

        # Initialize the Firebase Admin SDK
        cred = credentials.Certificate(firebase_cert_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully!")

        # Access Firestore
        db = firestore.client()
        print("Connected to Firestore!")

        return db

    except Exception as e:
        print("An error occurred:", e)
        return None

def check_user_exists(email: str):
    users_collection = db.collection("users")
    query = users_collection.where("email", "==", email)
    results = list(query.stream())
    return results[0].to_dict() if results else None

def check_email_exists(email: str):
    users_collection = db.collection("users")
    query = users_collection.where("email", "==", email)
    results = list(query.stream())
    return results[0].to_dict() if results else None

def register_new_user(username: str, email: str, password: str):
    users_collection = db.collection("users")
    users_collection.add({
        "username": username,
        "email": email,
        "password": password,
        "profile_picture": "",
        "bio": "No bio yet.",
        "followers": [],
        "following": []
    })
    return check_user_exists(email)

def create_posts(username: str, content: str):
    posts_collection = db.collection("posts")
    posts_collection.add({
        "username": username,                   
        "content": content,   
        "media": "",
        "likes": [],
        "comments": [],
        "created": str(datetime.date.today())
    })

# Initialize Firestore globally
db = initialize_firebase()
