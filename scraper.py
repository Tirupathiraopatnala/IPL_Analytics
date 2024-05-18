import requests
from bs4 import BeautifulSoup
import csv

players = []
roles = []
team = []
images = []

csv_file = "currentsquad.csv"


# Specify the URL of the website you want to scrape
url_list = [['https://www.iplt20.com/teams/chennai-super-kings','Chennai Super Kings'],
            ['https://www.iplt20.com/teams/delhi-capitals','Delhi Capitals'],
            ['https://www.iplt20.com/teams/gujarat-titans','Gujarat Titans'],
            ['https://www.iplt20.com/teams/kolkata-knight-riders','Kolkata Knight Riders'],
            ['https://www.iplt20.com/teams/lucknow-super-giants','Lucknow Super Giants'],
            ['https://www.iplt20.com/teams/mumbai-indians','Mumbai Indians'],
            ['https://www.iplt20.com/teams/punjab-kings','Punjab Kings'],
            ['https://www.iplt20.com/teams/rajasthan-royals','Rajasthan Royals'],
            ['https://www.iplt20.com/teams/royal-challengers-bangalore','Royal Challengers Bangalore'],
            ['https://www.iplt20.com/teams/sunrisers-hyderabad','Sunrisers Hyderabad']]

for url in url_list:
    # Send a GET request to the URL
    response = requests.get(url[0])
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract specific information from the webpage
    divs = soup.find_all('div', class_='ih-p-name')
    spans = soup.find_all('span', class_='d-block w-100 text-center')
    image_urls = soup.find_all('div', class_='ih-p-img')

    # Add the content of the divs into a list
    for div in divs:
        players.append(div.text.strip())
        
    for span in spans:
        roles.append(span.text.strip())
        team.append(url[1])
        
    for image in image_urls:
        img_tag = image.find('img')
        if img_tag:
            # Extract the 'src' attribute from the img tag
            images.append(img_tag.get('src'))

# Merge the lists
players_list = zip(players,roles,team,images)

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Name', 'Role', 'Team', 'ImageUrl'])
    # Write data
    writer.writerows(players_list)

print(f"CSV file '{csv_file}' created successfully.")