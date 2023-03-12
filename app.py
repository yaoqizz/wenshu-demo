import os
import openai
import json
from flask import Flask, redirect, render_template, request, url_for, make_response


app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

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
        history = request.cookies.get("history")
        if history is not None:
            history = json.loads(history)
        else:
            history = []
        history.append({"question": p, "response": response.choices[0].text})
        response = make_response(redirect(url_for("index", result=response.choices[0].text)))
        response.set_cookie("history", json.dumps(history))
        return response

    result = request.args.get("result")
    history = request.cookies.get("history")
    if history is not None:
        history = json.loads(history)
    else:
        history = []
    return render_template("index.html", result=result, history=history)

def generate_prompt(prompt):
    cap_prompt = prompt.capitalize()
    return f"你是一个人工智能客服：: {cap_prompt}\n "
    # return cap_prompt
