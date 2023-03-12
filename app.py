import os
import openai
from flask import Flask, redirect, render_template, request, url_for, make_response
import json
import time
import threading

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

HISTORY_DIR = "history"

def load_history(ip_address):
    history_file = f"{HISTORY_DIR}/{ip_address}.json"
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
        return history
    except:
        return []

def save_history(ip_address, history):
    history_file = f"{HISTORY_DIR}/{ip_address}.json"
    with open(history_file, "w") as f:
        json.dump(history, f)

@app.route("/", methods=("GET", "POST"))
def index():
    history = []
    if request.method == "POST":
        p = request.form["prompt"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=p,
            temperature=0.6,
            max_tokens=1500
        )
        ip_address = request.remote_addr
        history = load_history(ip_address)
        history.append({"question": p, "response": response.choices[0].text})
        save_history(ip_address, history)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    ip_address = request.remote_addr
    history = load_history(ip_address)
    return render_template("index.html", result=result, history=history)

def save_history_periodic():
    while True:
        for history_file in os.listdir(HISTORY_DIR):
            if history_file.endswith(".json"):
                ip_address = history_file[:-5]
                history = load_history(ip_address)
                save_history(ip_address, history)
        time.sleep(60)

def generate_prompt(prompt):
    cap_prompt = prompt.capitalize()
    return f"你是一个人工智能客服：: {cap_prompt}\n "

if __name__ == '__main__':
    app.run()
    save_history_thread = threading.Thread(target=save_history_periodic)
    save_history_thread.start()
