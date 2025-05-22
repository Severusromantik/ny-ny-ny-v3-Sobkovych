from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector

app = FastAPI()

# Конфігурація БД
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "my_password",
    "database": "mydb"
}

# ───────────── МОДЕЛІ ─────────────
class ExpertiseCategoryBase(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ExpertiseCategory(ExpertiseCategoryBase):
    id: int

class RoleBase(BaseModel):
    name: str
    description: Optional[str]

class Role(RoleBase):
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
    return {"message": "Expertise category created"}

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
    return {"message": "Expertise category updated"}

@app.delete("/expertise-categories/{category_id}")
def delete_expertise_category(category_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ExpertiseCategory WHERE id=%s", (category_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Expertise category deleted"}

# ───────────── ENDPOINTS: Role ─────────────
@app.get("/roles", response_model=List[Role])
def get_roles():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Role")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return roles

@app.post("/roles", status_code=201)
def create_role(role: RoleBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Role (name, description) VALUES (%s, %s)",
        (role.name, role.description)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Role created"}

@app.put("/roles/{role_id}")
def update_role(role_id: int, role: RoleBase):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Role SET name=%s, description=%s WHERE id=%s",
        (role.name, role.description, role_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Role updated"}

@app.delete("/roles/{role_id}")
def delete_role(role_id: int):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Role WHERE id=%s", (role_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Role deleted"}
