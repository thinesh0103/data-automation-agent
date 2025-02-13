from fastapi import FastAPI, HTTPException
import os
import json
import subprocess
from pathlib import Path

app = FastAPI()

DATA_DIR = "/data"

@app.post("/run")
async def run_task(task: str):
    """Executes a task based on a plain-English description."""
    try:
        result = execute_task(task)
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    """Reads the content of a file."""
    full_path = Path(DATA_DIR) / path.lstrip("/")
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(full_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}

def execute_task(task: str):
    """Parses and executes tasks."""
    if "count the number of Wednesdays" in task.lower():
        return count_wednesdays("/data/dates.txt", "/data/dates-wednesdays.txt")
    elif "sort contacts" in task.lower():
        return sort_contacts("/data/contacts.json", "/data/contacts-sorted.json")
    else:
        raise ValueError("Unknown task")

def count_wednesdays(input_file, output_file):
    from datetime import datetime
    with open(input_file, "r") as f:
        dates = [line.strip() for line in f.readlines()]
    count = sum(1 for d in dates if datetime.strptime(d, "%Y-%m-%d").weekday() == 2)
    with open(output_file, "w") as f:
        f.write(str(count))
    return f"Wrote {count} Wednesdays to {output_file}"

def sort_contacts(input_file, output_file):
    with open(input_file, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    return f"Sorted contacts saved to {output_file}"

def secure_path(file_path):
    """Ensure the file is within /data/."""
    full_path = Path(DATA_DIR) / file_path.lstrip("/")
    if not full_path.resolve().is_relative_to(DATA_DIR):
        raise ValueError("Access to files outside /data/ is restricted.")
    return full_path
