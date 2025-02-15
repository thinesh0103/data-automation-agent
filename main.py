from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import datetime
import re
from dateutil import parser
import os
import json

app = FastAPI()

class TaskRequest(BaseModel):
    task: str
    
def markdown_to_html() -> str:

    try:
        with open(r"/data/format.md", "r") as file:
            text = file.read()
        html = markdown.markdown(text)
    except Exception as e:
        raise Exception(f"Error occurred while converting markdown to html: {str(e)}")

    try:
        with open(r"/data/md_to_html.html", "w") as file:
             file.write(html)
    except Exception as e:
            raise Exception(f"Error occurred while writing html to file: {str(e)}")
    return html



def title_md():
    index = {}

    for root, _, files in os.walk(r"/data/docs/"):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            relative_path = os.path.relpath(file_path, r"/data/docs/")
                            relative_path_with_slash = relative_path.replace("\\", "/")
                            index[relative_path_with_slash] = title
                            break

    with open(r"/data/docs/index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

def recent_lines():

    log_files = [f for f in os.listdir(r"/data/logs/") if f.endswith(".log")]

    log_files = [os.path.join(r"/data/logs/", f) for f in log_files]

    log_files.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    recent_files = log_files[:10]

    with open(r"/data/logs-recent.txt" , "w") as outfile:
        for log_file in recent_files:
            with open(log_file, "r") as infile:
                first_line = infile.readline().strip()
                outfile.write(first_line + "\n")


def sort_contacts():
    with open(r"/data/contacts.json", "r") as infile:
        data = json.load(infile)

    sorted_data = sorted(data, key=lambda x: (x["last_name"], x["first_name"]))

    with open(r"/data/contacts-sorted.json", "w") as outfile:
        json.dump(sorted_data, outfile, indent=4)

def read_file_content(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# Function to format a Markdown file using Prettier
def format_markdown(file_path: str) -> str:
    path = Path(file_path)
    
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        result = subprocess.run(
            ["npx", "prettier@3.4.2", "--write", str(path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Prettier Error: {result.stderr}")
        return f"Formatted {file_path} successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running Prettier: {str(e)}")


def count_weekdays(file_path: str, target_weekday: int) -> int:
    path = Path(file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with path.open("r", encoding="utf-8") as file:
            dates = file.readlines()
        
        count = 0
        for date_str in dates:
            date_str = date_str.strip()
            if not date_str:
                continue  # Skip empty lines
            
            try:
                parsed_date = parser.parse(date_str, dayfirst=False)
                if parsed_date.weekday() == target_weekday:
                    count += 1
            except ValueError:
                print(f"Skipping invalid date format: {date_str}")  # Debugging

        return count

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


def process_task(task: str) -> str:
    task = task.lower()  # Normalize case for comparison
    
    if "format" in task and "prettier" in task:
        return format_markdown("/data/format.md")
    elif "wednesdays" in task:
        count = count_weekdays("/data/dates.txt", 2)  # Wednesday (0=Monday, 2=Wednesday)
        Path("/data/dates-wednesdays.txt").write_text(str(count), encoding="utf-8")
        return f"Total Wednesdays: {count}"
    elif "contacts sorted" in task:
        sort_contacts()
        return "Contacts have been sorted."
    elif "recent" in task and "log" in task:
        recent_lines()
        return "Recent log file lines processed."
    elif "title" in task:
    	title_md()
    	return "Done"
    elif "to html" in task:
    	markdown_to_html()
    	return "Successfully converted markdown to html"
    else:
        return "Unknown task."

@app.post("/run")
def run_task(task_request: TaskRequest):
    return {"message": process_task(task_request.task)}
