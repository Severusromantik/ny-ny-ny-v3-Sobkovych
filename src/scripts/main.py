from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from datetime import datetime

app = FastAPI()

# ───────────── Конфігурація бази даних ─────────────
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "abcdefu4849",
    "database": "mydb"
}

# ───────────── Моделі ─────────────

class ExpertiseCategoryBase(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ExpertiseCategory(ExpertiseCategoryBase):
    id: int

class SurveySessionBase(BaseModel):
    User_id: int
    Quiz_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    status: Optional[str]

class SurveySession(SurveySessionBase):
    id: int

# ───────────── ENDPOINTS: ExpertiseCategory ─────────────

@app.get("/expertise-categories", response_model=List[ExpertiseCategory])
def get_expertise_categories():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ExpertiseCategory")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

@app.post("/expertise-categories", status_code=201)
def create_expertise_category(category: ExpertiseCategoryBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ExpertiseCategory (name, description) VALUES (%s, %s)",
        (category.name, category.description)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "ExpertiseCategory created"}

@app.put("/expertise-categories/{category_id}")
def update_expertise_category(category_id: int, category: ExpertiseCategoryBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ExpertiseCategory SET name=%s, description=%s WHERE id=%s",
        (category.name, category.description, category_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "ExpertiseCategory updated"}

@app.delete("/expertise-categories/{category_id}")
def delete_expertise_category(category_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ExpertiseCategory WHERE id=%s", (category_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "ExpertiseCategory deleted"}

# ───────────── ENDPOINTS: SurveySession ─────────────

@app.get("/survey-sessions", response_model=List[SurveySession])
def get_survey_sessions():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM SurveySession")
    sessions = cursor.fetchall()
    cursor.close()
    conn.close()
    return sessions

@app.post("/survey-sessions", status_code=201)
def create_survey_session(session: SurveySessionBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO SurveySession (User_id, Quiz_id, started_at, completed_at, status) VALUES (%s, %s, %s, %s, %s)",
        (session.User_id, session.Quiz_id, session.started_at, session.completed_at, session.status)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "SurveySession created"}

@app.put("/survey-sessions/{session_id}")
def update_survey_session(session_id: int, session: SurveySessionBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE SurveySession SET User_id=%s, Quiz_id=%s, started_at=%s, completed_at=%s, status=%s WHERE id=%s",
        (session.User_id, session.Quiz_id, session.started_at, session.completed_at, session.status, session_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "SurveySession updated"}

@app.delete("/survey-sessions/{session_id}")
def delete_survey_session(session_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SurveySession WHERE id=%s", (session_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "SurveySession deleted"}
