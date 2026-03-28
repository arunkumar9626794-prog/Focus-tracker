import time
import json
from datetime import datetime

start_time = None
DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def start_focus():
    global start_time
    start_time = time.time()
    print("Session started...")

def stop_focus():
    global start_time

    if start_time is None:
        print("You didn't start a session!")
        return

    end_time = time.time()
    duration = end_time - start_time
    minutes = round(duration / 60, 2)

    type_choice = input("Enter type (focus/distraction): ").lower()

    if type_choice not in ["focus", "distraction"]:
        print("Invalid input, defaulting to focus")
        type_choice = "focus"

    session = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "duration": minutes,
        "type": type_choice
    }

    data = load_data()
    data.append(session)
    save_data(data)

    print(f"Saved: {minutes} mins as {type_choice}")

    start_time = None

def view_report():
    data = load_data()
    if not data:
        print("No data found")
        return

    focus_time = 0
    distraction_time = 0

    for item in data:
        if item["type"] == "focus":
            focus_time += item["duration"]
        else:
            distraction_time += item["duration"]

    print("\n--- REPORT ---")
    print(f"Focus Time: {round(focus_time,2)} mins")
    print(f"Distraction Time: {round(distraction_time,2)} mins")

def view_today_report():
    data = load_data()
    if not data:
        print("No data found")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    focus_time = 0
    distraction_time = 0

    for item in data:
        if item["date"] == today:
            if item["type"] == "focus":
                focus_time += item["duration"]
            else:
                distraction_time += item["duration"]

    total_time = focus_time + distraction_time

    print("\n--- TODAY REPORT ---")
    print(f"Today's Focus: {round(focus_time,2)} mins")
    print(f"Today's Distraction: {round(distraction_time,2)} mins")

    # 🔥 Focus Score
    if total_time > 0:
        score = (focus_time / total_time) * 100
        print(f"Focus Score: {round(score,2)}%")

        # 🔥 Smart Suggestions
        print("\n--- SUGGESTION ---")

        if distraction_time > focus_time:
            print("⚠️ You are wasting too much time!")

        if score > 70:
            print("🔥 Great focus! Keep it up!")
        elif score < 40:
            print("❌ Poor focus. Reduce distractions.")

        if focus_time > 120:
            print("💪 Excellent consistency today!")

    else:
        print("No sessions today")

# MENU
while True:
    print("\n1. Start")
    print("2. Stop")
    print("3. Report")
    print("4. Today Report")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        start_focus()
    elif choice == "2":
        stop_focus()
    elif choice == "3":
        view_report()
    elif choice == "4":
        view_today_report()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice")
