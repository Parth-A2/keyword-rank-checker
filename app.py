from flask import Flask, request, render_template_string
from serpapi.google_search import GoogleSearch
from urllib.parse import urlparse
import os

app = Flask(__name__)

# Your SerpApi Key
API_KEY = "51d0be0f94fb75c28e3358a0e8160b3cc5538a95e3210d07e938d7a65a50c5a7"


def normalize_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def find_ranking(keyword, target_domain, max_results=300):

    target_domain = target_domain.lower().replace("www.", "")

    for start in range(0, max_results, 10):

        print(f"Checking {start + 1} to {start + 10}")

        params = {
            "engine": "google",
            "q": keyword,
            "api_key": API_KEY,
            "num": 10,
            "start": start
        }

        try:

            search = GoogleSearch(params)
            results = search.get_dict()

            print("API RESPONSE:", results)

            # organic_results = results.get("organic_results", [])
            return str(results)

            if not organic_results:
                break

            for result in organic_results:

                link = result.get("link", "")

                if not link:
                    continue

                result_domain = normalize_domain(link)

                actual_position = result.get("position")

                print(actual_position, result_domain)

                # Match domain
                if target_domain in result_domain:
                    return actual_position

        except Exception as e:
            return f"Error: {e}"

    return f"Domain is not ranking in top {max_results} Google results"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Keyword Ranking Checker</title>

    <style>

        body{
            font-family: Arial;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }

        input{
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
        }

        button{
            padding: 12px 20px;
            cursor: pointer;
        }

        .result{
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
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

        keyword = request.form["keyword"]
        domain = request.form["domain"]

        ranking = find_ranking(keyword, domain)

    return render_template_string(HTML, ranking=ranking)


if __name__ == "__main__":
    app.run(debug=True)