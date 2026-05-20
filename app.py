from flask import Flask, request, render_template_string
from serpapi.google_search import GoogleSearch
from urllib.parse import urlparse
import traceback

app = Flask(__name__)

API_KEY = "YOUR_SERPAPI_KEY_HERE"


def normalize_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
    except Exception as e:
        return f"DOMAIN_PARSE_ERROR: {e}"


def find_ranking(keyword, target_domain, max_results=300):

    logs = []

    def log(msg):
        logs.append(str(msg))

    try:
        log("STEP 1: Function started")
        log(f"Keyword: {keyword}")
        log(f"Target Domain: {target_domain}")

        target_domain = target_domain.lower().replace("www.", "")

        position_counter = 0

        for start in range(0, max_results, 10):

            log(f"STEP 2: Fetching results {start + 1} to {start + 10}")

            params = {
                "engine": "google",
                "q": keyword,
                "api_key": API_KEY,
                "num": 10,
                "start": start
            }

            log(f"STEP 3: Params built: {params}")

            search = GoogleSearch(params)
            results = search.get_dict()

            log("STEP 4: API response received")

            organic_results = results.get("organic_results", [])

            log(f"STEP 5: Organic results count: {len(organic_results)}")

            if not organic_results:
                log("No organic results found, stopping loop")
                break

            for result in organic_results:

                position_counter += 1

                link = result.get("link", "")
                domain = normalize_domain(link)

                log(f"Result {position_counter}: {domain}")

                if target_domain in domain:
                    log("MATCH FOUND!")
                    return f"FOUND at position {position_counter}", logs

        log("STEP FINAL: Not found in top results")

        return f"Not ranking in top {max_results}", logs

    except Exception as e:
        log("ERROR OCCURRED")
        log(traceback.format_exc())
        return f"Error: {e}", logs


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Debug Ranking Checker</title>

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

        .logs {
            margin-top: 20px;
            background: #111;
            color: #0f0;
            padding: 15px;
            font-size: 13px;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: scroll;
        }

        .error {
            color: red;
        }
    </style>
</head>

<body>

    <h1>Debug Keyword Ranking Checker</h1>

    <form method="POST">

        <input type="text" name="keyword" placeholder="Enter Keyword" required>
        <input type="text" name="domain" placeholder="Enter Domain" required>

        <button type="submit">Check Ranking</button>

    </form>

    {% if ranking %}
        <div class="result">
            RESULT: {{ ranking }}
        </div>
    {% endif %}

    {% if logs %}
        <div class="logs">
{% for log in logs %}
{{ log }}
{% endfor %}
        </div>
    {% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    ranking = None
    logs = []

    if request.method == "POST":

        keyword = request.form.get("keyword")
        domain = request.form.get("domain")

        ranking, logs = find_ranking(keyword, domain)

    return render_template_string(HTML, ranking=ranking, logs=logs)


if __name__ == "__main__":
    app.run(debug=True)