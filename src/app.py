"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
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
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    from fastapi import FastAPI, HTTPException
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import RedirectResponse
    from sqlmodel import select, Session
    from pathlib import Path
    import os

    from .db import create_db_and_tables, engine
    from .models import Activity, Participant


    app = FastAPI(title="Mergington High School API",
                  description="API for viewing and signing up for extracurricular activities")

    # Mount the static files directory
    current_dir = Path(__file__).parent
    app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent, "static")), name="static")


    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()
        # Seed DB if empty
        with Session(engine) as session:
            has_any = session.exec(select(Activity)).first()
            if not has_any:
                from .seed import seed_activities

                seed_activities(session)


    @app.get("/")
    def root():
        return RedirectResponse(url="/static/index.html")


    @app.get("/activities")
    def get_activities():
        with Session(engine) as session:
            activities = session.exec(select(Activity)).all()
            result = []
            for a in activities:
                # fetch participants
                participants = session.exec(select(Participant).where(Participant.activity_id == a.id)).all()
                result.append(
                    {
                        "id": a.id,
                        "name": a.name,
                        "description": a.description,
                        "schedule": a.schedule,
                        "max_participants": a.max_participants,
                        "participants": [p.email for p in participants],
                    }
                )
            return result


    @app.post("/activities/{activity_name}/signup")
    def signup_for_activity(activity_name: str, email: str):
        with Session(engine) as session:
            activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")

            participants = session.exec(select(Participant).where(Participant.activity_id == activity.id)).all()
            if email in [p.email for p in participants]:
                raise HTTPException(status_code=400, detail="Student is already signed up")

            if activity.max_participants and len(participants) >= activity.max_participants:
                raise HTTPException(status_code=400, detail="Activity is full")

            p = Participant(email=email, activity_id=activity.id)
            session.add(p)
            session.commit()
            return {"message": f"Signed up {email} for {activity_name}"}


    @app.delete("/activities/{activity_name}/unregister")
    def unregister_from_activity(activity_name: str, email: str):
        with Session(engine) as session:
            activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
            if not activity:
                raise HTTPException(status_code=404, detail="Activity not found")

            participant = session.exec(
                select(Participant).where(Participant.activity_id == activity.id).where(Participant.email == email)
            ).first()
            if not participant:
                raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

            session.delete(participant)
            session.commit()
            return {"message": f"Unregistered {email} from {activity_name}"}
