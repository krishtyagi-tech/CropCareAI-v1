import sqlite3
from datetime import datetime

DB_NAME = "database/cropcare.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# =====================================================
# CREATE TABLES
# =====================================================

# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------
    # Crops Table
    # -----------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crops(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_uid TEXT NOT NULL,

        crop_name TEXT NOT NULL,

        plant_id TEXT UNIQUE NOT NULL,

        field_name TEXT,

        planting_date TEXT

    )
    """)

    # -----------------------
    # Monitoring Table
    # -----------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoring(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        crop_id INTEGER,

        image_path TEXT,

        disease TEXT,

        status TEXT,

        confidence REAL,

        city TEXT,

        temperature REAL,

        humidity REAL,

        pressure REAL,

        wind_speed REAL,

        weather TEXT,

        ai_chat TEXT,

        scan_date TEXT,

        FOREIGN KEY(crop_id)
        REFERENCES crops(id)

    )
    """)

    conn.commit()
    conn.close()
# =====================================================
# ADD CROP
# =====================================================

# =====================================================
# ADD CROP
# =====================================================

def add_crop(

    user_uid,

    crop_name,

    plant_id,

    field_name,

    planting_date

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO crops(

            user_uid,

            crop_name,

            plant_id,

            field_name,

            planting_date

        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (

            user_uid,

            crop_name,

            plant_id,

            field_name,

            planting_date

        )
    )

    conn.commit()
    conn.close()
# =====================================================
# GET ALL CROPS
# =====================================================

def get_crops():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM crops
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# For app.py
def get_all_crops():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, plant_id, crop_name
        FROM crops
        ORDER BY plant_id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# GET CROP BY PLANT ID
# =====================================================

def get_crop_by_plant_id(plant_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM crops
        WHERE plant_id=?
        """,
        (plant_id,)
    )

    crop = cursor.fetchone()

    conn.close()

    return crop


# =====================================================
# SAVE SCAN
# =====================================================

def save_scan(

    crop_id,

    image_path,

    disease,

    status,

    confidence,

    city,

    temperature,

    humidity,

    pressure,

    wind_speed,

    weather,

    ai_chat

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO monitoring(

        crop_id,

        image_path,

        disease,

        status,

        confidence,

        city,

        temperature,

        humidity,

        pressure,

        wind_speed,

        weather,

        ai_chat,

        scan_date

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        crop_id,

        image_path,

        disease,

        status,

        float(confidence),   # <-- convert HERE

        city,

        temperature,

        humidity,

        pressure,

        wind_speed,

        weather,

        ai_chat,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
)
    conn.commit()
    conn.close()


# =====================================================
# GET SCANS OF A CROP
# =====================================================

def get_scans(crop_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM monitoring
        WHERE crop_id=?
        ORDER BY scan_date DESC
        """,
        (crop_id,)
    )

    scans = cursor.fetchall()

    conn.close()

    return scans
def get_scans_with_crop():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            monitoring.id,

            monitoring.crop_id,

            crops.crop_name,

            crops.plant_id,

            crops.field_name,

            monitoring.image_path,

            monitoring.disease,

            monitoring.status,

            monitoring.confidence,

            monitoring.city,

            monitoring.temperature,

            monitoring.humidity,

            monitoring.pressure,

            monitoring.wind_speed,

            monitoring.weather,

            monitoring.ai_chat,

            monitoring.scan_date

        FROM monitoring

        INNER JOIN crops

        ON monitoring.crop_id = crops.id

        ORDER BY crops.crop_name,
                 crops.plant_id,
                 monitoring.scan_date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_crop_groups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT crop_name
        FROM crops
        ORDER BY crop_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

def get_plants_by_crop(crop_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM crops
        WHERE crop_name=?
        ORDER BY plant_id
        """,
        (crop_name,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Plants
    cursor.execute("SELECT COUNT(*) FROM crops")
    total_plants = cursor.fetchone()[0]

    # Total Scans
    cursor.execute("SELECT COUNT(*) FROM monitoring")
    total_scans = cursor.fetchone()[0]

    # Latest scan of every plant
    cursor.execute("""
        SELECT m.status

        FROM monitoring m

        INNER JOIN (

            SELECT crop_id,
                   MAX(scan_date) AS latest_scan

            FROM monitoring

            GROUP BY crop_id

        ) latest

        ON m.crop_id = latest.crop_id
        AND m.scan_date = latest.latest_scan
    """)

    latest_status = cursor.fetchall()

    healthy = sum(
        1 for row in latest_status
        if "Healthy" in row[0]
    )

    diseased = sum(
        1 for row in latest_status
        if "Diseased" in row[0]
    )

    conn.close()

    return {
        "plants": total_plants,
        "scans": total_scans,
        "healthy": healthy,
        "diseased": diseased
    }
def get_current_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            crops.id,

            crops.crop_name,

            crops.plant_id,

            crops.field_name,

            monitoring.disease,

            monitoring.status,

            monitoring.scan_date

        FROM monitoring

        INNER JOIN crops
            ON monitoring.crop_id = crops.id

        INNER JOIN(

            SELECT
                crop_id,
                MAX(scan_date) latest_scan

            FROM monitoring

            GROUP BY crop_id

        ) latest

        ON monitoring.crop_id = latest.crop_id

        AND monitoring.scan_date = latest.latest_scan

        WHERE monitoring.status LIKE '%Diseased%'

        ORDER BY monitoring.scan_date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_health_distribution():

    stats = get_dashboard_stats()

    return {
        "Healthy": stats["healthy"],
        "Diseased": stats["diseased"]
    }
def get_recent_activity(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            crops.crop_name,

            crops.plant_id,

            monitoring.disease,

            monitoring.status,

            monitoring.scan_date

        FROM monitoring

        INNER JOIN crops

        ON monitoring.crop_id = crops.id

        ORDER BY monitoring.scan_date DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_complete_plant_history(crop_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            crops.crop_name,
            crops.plant_id,
            crops.field_name,

            monitoring.image_path,
            monitoring.disease,
            monitoring.status,
            monitoring.confidence,

            monitoring.city,
            monitoring.temperature,
            monitoring.humidity,
            monitoring.pressure,
            monitoring.wind_speed,
            monitoring.weather,

            monitoring.ai_chat,
            monitoring.scan_date

        FROM monitoring

        INNER JOIN crops

        ON monitoring.crop_id = crops.id

        WHERE monitoring.crop_id = ?

        ORDER BY monitoring.scan_date ASC
        """,
        (crop_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

import os

def delete_scan(scan_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Get image path before deleting
    cursor.execute(
        """
        SELECT image_path
        FROM monitoring
        WHERE id = ?
        """,
        (scan_id,)
    )

    row = cursor.fetchone()

    if row:

        image_path = row[0]

        print("Image Path:", image_path)
        print("Exists:", os.path.exists(image_path))

        if image_path and os.path.exists(image_path):

            os.remove(image_path)

    # Delete scan from database
    cursor.execute(
        """
        DELETE FROM monitoring
        WHERE id = ?
        """,
        (scan_id,)
    )

    conn.commit()
    conn.close()

def delete_crop(crop_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Delete all scans of this crop
    cursor.execute(
        """
        DELETE FROM monitoring
        WHERE crop_id = ?
        """,
        (crop_id,)
    )

    # Delete crop
    cursor.execute(
        """
        DELETE FROM crops
        WHERE id = ?
        """,
        (crop_id,)
    )

    conn.commit()
    conn.close()
    
def get_crop_distribution():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            crop_name,
            COUNT(*)
        FROM crops
        GROUP BY crop_name
        ORDER BY crop_name
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows