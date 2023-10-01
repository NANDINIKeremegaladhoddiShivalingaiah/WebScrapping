import requests
from bs4 import BeautifulSoup
import json
import markdownify

# Function to scrape and convert HTML tables to Markdown
def html_table_to_markdown(html_table):
    return markdownify.html_to_markdown(str(html_table))

# Initialize the list to store scraped data
data_list = []

# URL of the website
base_url = "https://indiacorplaw.in/page/"

# Iterate through the first 5 pages
for page_num in range(1, 6):
    url = f"{base_url}{page_num}"

    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    
    articles = soup.find_all("article")

    # Iterate through each article
    for article in articles:
        
        title = article.find("h2").text.strip()

        typology_buttons = article.find_all("a", class_="typology-button")
        read_on_content = []

        for button in typology_buttons:
            button_text = button.text.strip()
            if button_text == "Read on":
                
                read_on_url = button.get("href")
                read_on_response = requests.get(read_on_url)
                read_on_soup = BeautifulSoup(read_on_response.text, "html.parser")
                read_on_article = read_on_soup.find("article")
                read_on_content.append(read_on_article.text.strip())

                read_on_content[-1] = read_on_content[-1].replace('\n', ' ').strip()


       
        tables = article.find_all("table")
        for table in tables:
            table.replace_with(html_table_to_markdown(table))

        
        data_list.append({
            "title": title,
            "read_on_content": read_on_content,
        })

# Save the scraped data to a JSON file
with open("scraped_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("Scraping completed and data saved to scraped_data.json")
