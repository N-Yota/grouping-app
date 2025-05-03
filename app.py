from flask import Flask, request, render_template
from my_grouping_tool.main import run_from_url

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        try:
            result = run_from_url(url)  # ← ここだけでOK！
            print("DEBUG 出力:", result)  # ← これを入れる

        except Exception as e:
            result = f"エラーが発生しました: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


