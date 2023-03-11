import os

import openai
from flask import Flask, redirect, render_template, request, url_for
# from flask_cors import CORS
app = Flask(__name__)
# CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

history = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        p = request.form["prompt"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(p),
            temperature=0.6,
            max_tokens=500
        )
        history.append({"question": p, "response": response.choices[0].text})
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result, history=history)


def generate_prompt(prompt):
    cap_prompt = prompt.capitalize()
    return f"你是一个人工智能客服：: {cap_prompt}\n "
