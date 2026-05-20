from serpapi import GoogleSearch
from urllib.parse import urlparse

# Your SerpApi Key
API_KEY = "51d0be0f94fb75c28e3358a0e8160b3cc5538a95e3210d07e938d7a65a50c5a7"


def normalize_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Remove www.
    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def find_ranking(keyword, target_domain, max_results=300):

    # Normalize target domain
    target_domain = target_domain.lower().replace("www.", "")

    # Ranking position counter
    position = 1

    # Search Google results page by page
    for start in range(0, max_results, 10):

        print(f"\nChecking results {start + 1} to {start + 10}...")

        params = {
            "engine": "google",
            "q": keyword,
            "api_key": API_KEY,
            "num": 10,
            "start": start
        }

        try:

            # Fetch search results
            search = GoogleSearch(params)
            results = search.get_dict()

            # Get organic results
            organic_results = results.get("organic_results", [])

            # Stop if no more results found
            if not organic_results:
                print("\nNo more Google results found.")
                break

            # Loop through results
            for result in organic_results:

                link = result.get("link", "")
                result_domain = normalize_domain(link)

                # Print current result
                print(f"{position}. {result_domain}")

                # Check if target domain matches
                if target_domain in result_domain:
                    return position

                position += 1

        except Exception as e:
            return f"Error: {e}"

        return f"Domain is not ranking in top {max_results} Google results"


if __name__ == "__main__":

    print("=== Keyword Ranking Checker ===\n")

    keyword = input("Enter Keyword: ").strip()
    domain = input("Enter Domain: ").strip()

    print("\nSearching Google Rankings...\n")

    ranking = find_ranking(keyword, domain, 300)

    print("\n========================")
    print("Keyword :", keyword)
    print("Domain  :", domain)
    print("Ranking :", ranking)
    print("========================")