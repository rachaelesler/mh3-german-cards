"""
Returns the German name for MH3 cards, along with English name, typeline, 
and oracle text. 
By Rachael Esler

"""
import requests
import time
import csv

def is_valid_request(response): 
    if response.status_code != 200:
        print("Error fetching data: {0}".format(response.status_code))
        return False
    return True

def get_recent_cards(set_code, lang, count):
    url = "https://api.scryfall.com/cards/search"
    query = "set:{0} lang:{1}".format(set_code, lang)
    params = {
        'q': query,
        'order': 'released',
        'dir': 'desc',
        'unique': 'prints',
        'page': 1
    }
    response = requests.get(url, params=params)
    
    if(not is_valid_request(response)): 
        return []
    
    data = response.json()
    cards = data.get('data', [])
    
    # Fetch the next page if less than count cards are retrieved
    while len(cards) < count and data.get('has_more'):
        params['page'] += 1
        time.sleep(0.1)  # 100 ms delay
        response = requests.get(url, params=params)
        if(not is_valid_request(response)): 
            break
        data = response.json()
        cards.extend(data.get('data', []))
    
    return cards[:count]

def write_to_csv(cards):
    with open('./recent_cards.csv', 'w', newline='', encoding='utf-8') as csv_file:
        field_names = ["Deutsch","English","Typeline","Oracle"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter='^')
        
        writer.writeheader()
        for card in cards:
            writer.writerow({'Deutsch': card['printed_name'], 'English': card['name'], 'Typeline': card['type_line'], "Oracle":card["oracle_text"] if 'oracle_text' in card else ''})

def main():
    set_code = "mh3"
    count=10
    # english_cards = get_recent_cards(set_code, "en", count)
    german_cards = get_recent_cards(set_code, "de", count)
    german_cards_sorted = sorted(german_cards, key=lambda x: x['printed_name'])

    print("Deutsch;English;Typeline;Oracle")
    write_to_csv(german_cards_sorted)
    for card in german_cards_sorted:
        print("{0};{1};{2};{3}".format(card["printed_name"], card["name"], card["type_line"], card["oracle_text"] if 'oracle_text' in card else ''))

if __name__ == "__main__":
    main()
