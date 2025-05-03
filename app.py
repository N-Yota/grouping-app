import os
from flask import Flask, request, render_template
from my_grouping_tool.main import run_from_url

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        try:
            result = run_from_url(url)
        except Exception as e:
            result = f"エラーが発生しました: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが指定するPORTを使う
    app.run(host="0.0.0.0", port=port)



