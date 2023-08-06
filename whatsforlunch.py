import requests
from bs4 import BeautifulSoup
from datetime import datetime

days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

def print_menu():
    print('╔═════════════════════════════════════════════╗')
    print('║         Select what you want to see:        ║')
    print('║                                             ║')
    print('║               1. Edison today               ║')
    print('║               2. Edison week                ║')
    print('║               3. Grenden today              ║')
    print('║               4. Grenden week               ║')
    print('║                                             ║')
    print('╚═════════════════════════════════════════════╝')


def get_data(url):
    # Send a GET request to the URL
    response = requests.get(url, verify=False)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def print_week_edison(soup):
    # Find the menu items
    menu_items = soup.find_all('div', class_='container menu')

    for day in days:
        day_element = soup.find('div', id=day)
        if day_element:
            menu_items = day_element.find_all('tr')
            print_day_edison(menu_items, day)


def print_day_edison(menu_items, day):

    print('══════════════════════════════════════════════════════════════════════════════════════════')
    print("Menu for", day.capitalize())
    print('------------------------------------------------------------------------------------------')

    for item in menu_items:
                course_type_element = item.find('td', class_='course_type')
                course_description_element = item.find('td', class_='course_description')
                course_price_element = item.find('td', class_='course_price')

                course_type = course_type_element.find('p').text.strip() if course_type_element else None
                course_description = course_description_element.find('p').text.strip() if course_description_element else None
                course_price = course_price_element.find('p').text.strip() if course_price_element else None

                print("Course Type:", course_type)
                print("Course Description:", course_description)
                print("Course Price:", course_price)
                print()


def print_day_grenden(menu_items, day):

    print('══════════════════════════════════════════════════════════════════════════════════════════')
    print("Menu for", day.capitalize())
    print('------------------------------------------------------------------------------------------')

    
    day_info = menu_items.find('strong', string=day.upper())
    if day_info:
        parent = day_info.parent
        for item in parent:
            print(item.get_text().strip())
            print()

def print_week_grenden(soup):
    menu_items = soup.find('div', class_='wpb_wrapper')
    for day in days: 
            print_day_grenden(menu_items, day)


# Main program loop
while True:
    print_menu()
    selection = input("Enter the number (1-2), or 'q' to quit: ")

    url_edison = "https://restaurangedison.se/lunch"
    url_grenden = "https://lund.pieplowsmat.se/grenden/"

    if selection == "q":
        break

    if selection == "1":
        soup = get_data(url_edison)
        dt = datetime.now()
        day = days[dt.isoweekday()-1]
        day_element = soup.find('div', id=day)
        menu_items = day_element.find_all('tr')
        print_day_edison(menu_items, day)

    if selection == "2":
        soup = get_data(url_edison)
        print_week_edison(soup)

    if selection == "3":
        soup = get_data(url_grenden)
        dt = datetime.now()
        #day = days[dt.isoweekday()-1]
        menu_items = soup.find('div', class_='wpb_wrapper')
        print_day_grenden(menu_items, "MONDAY")

    if selection == "4":
        soup = get_data(url_grenden)
        print_week_grenden(soup)