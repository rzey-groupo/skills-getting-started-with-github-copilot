"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball league and practice",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis lessons and competitive matches",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 12,
        "participants": ["jessica@mergington.edu", "chris@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["ryan@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore STEM concepts through experiments and research",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["lily@mergington.edu", "ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return JSONResponse(content=activities, headers={"Cache-Control": "no-store"})


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check that the student is currently signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not signed up for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
