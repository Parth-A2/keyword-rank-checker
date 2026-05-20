from flask import Flask, request, render_template_string
from serpapi.google_search import GoogleSearch
from urllib.parse import urlparse
import os

app = Flask(__name__)

API_KEY = "51d0be0f94fb75c28e3358a0e8160b3cc5538a95e3210d07e938d7a65a50c5a7"


def normalize_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def find_ranking(keyword, target_domain, max_results=300):

    target_domain = target_domain.lower().replace("www.", "")

    position_counter = 0

    try:

        for start in range(0, max_results, 10):

            params = {
                "engine": "google",
                "q": keyword,
                "api_key": API_KEY,
                "num": 10,
                "start": start
            }

            search = GoogleSearch(params)
            results = search.get_dict()

            organic_results = results.get("organic_results", [])

            if not organic_results:
                break

            for result in organic_results:

                position_counter += 1

                link = result.get("link", "")
                domain = normalize_domain(link)

                if target_domain in domain:
                    return f"Found at position {position_counter}"

        return f"Domain is not ranking in top {max_results} Google results"

    except Exception as e:
        return f"Error: {e}"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ranking Checker</title>

    <style>
        body {
            font-family: Arial;
            max-width: 800px;
            margin: 30px auto;
            padding: 20px;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }

        button {
            padding: 10px 15px;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
            color: green;
        }
    </style>
</head>

<body>

    <h1>Keyword Ranking Checker</h1>

    <form method="POST">

        <input 
            type="text" 
            name="keyword" 
            placeholder="Enter Keyword" 
            required
        >

        <input 
            type="text" 
            name="domain" 
            placeholder="Enter Domain" 
            required
        >

        <button type="submit">
            Check Ranking
        </button>

    </form>

    {% if ranking %}
        <div class="result">
            Ranking: {{ ranking }}
        </div>
    {% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    ranking = None

    if request.method == "POST":

        keyword = request.form.get("keyword")
        domain = request.form.get("domain")

        ranking = find_ranking(keyword, domain)

    return render_template_string(HTML, ranking=ranking)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )