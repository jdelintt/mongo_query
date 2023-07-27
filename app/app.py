import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
data = pd.read_json('./response.json')
# Define the keywords and their synonyms
upscale_keywords = ["cool", "barry"]
synonyms = {
    "ambiance": ["beautiful", "chill", "mindset", "WOD"],
    "small classes": ["crossfit", "athletes", "athlete"]
}


def is_upscale_website(website):
    if website is None:
        return False

    # Fetch the website content
    try:
        response = requests.get(website)
        response.raise_for_status()  # Check for any request errors
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch website content: {e}")
        return False

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get all text from the HTML content
    all_text = soup.get_text()

    # Combine all keywords and synonyms into a single list
    upscale_terms = upscale_keywords + \
        [syn for syn_list in synonyms.values() for syn in syn_list]

    # Check if any upscale term is present in the collected text
    return any(re.search(term, all_text, re.IGNORECASE) for term in upscale_terms)


# Rest of the code remains the same...
# Classify each gym as "upscale" or "generic" based on the website
for index, row in data.iterrows():
    website = row['website']
    if is_upscale_website(
            website):
        data.loc[index, "type"] = "upscale"
    else:
        data.loc[index, "type"] = "generic"
    print(data.loc[index, "type"])
data.to_csv('./data/gym_sa.csv')
