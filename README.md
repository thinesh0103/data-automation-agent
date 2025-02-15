# 🛠️ Usage

You can 🏃 tasks by 📤 a POST request to the /run 🔗 with a 📜 payload.

### 1️⃣ ✨ Format Markdown Using Prettier
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "📝 Format /data/format.md with ✨ Prettier 3.4.2"}'


### 2️⃣ 📆 Count Wednesdays in dates.txt
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "🔢 Count all 📆 Wednesdays in /data/dates.txt"}'


### 3️⃣ 📑 Sort Contacts from contacts.json
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "📇 Sort contacts and save to contacts-sorted.json"}'


### 4️⃣ 📜 Get Recent Log File Lines
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "📜 Get recent log file lines and save to logs-recent.txt"}'


### 5️⃣ 🏷️ Generate Titles Index from Markdown Files
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "📖 Generate titles index from markdown files"}'


### 6️⃣ 🔄 Convert Markdown to HTML
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "📄 Convert markdown to 🌐 HTML"}'


### 7️⃣ ❓ Handle Unknown Tasks
sh
📤 curl -X POST "http://localhost:8000/run" \
     -H "Content-Type: application/json" \
     -d '{"task": "🤷 Do something random"}'

#### 🔍 Expected Output:
json
{"message": "❓ Unknown task."}
