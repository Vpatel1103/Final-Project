# Vaidehi Patel
# 2154931

import csv
from datetime import datetime

# Converting the csv into proper dicitonaries to call and organize data
def import_data():
    manufact = {}
    prices = {}
    serviceDate = {}

    #Function for reading and storing thhe given csv files
    with open('ManufacturerList.csv', 'r') as file:
        list = csv.reader(file)
        for row in list:
            item = row[0]
            manufact[item] = {
                'manufacturer': row[1],
                'itemType': row[2],
                'damaged': row[3] 
            }
    with open('PriceList.csv', 'r') as file:
        list = csv.reader(file)
        for row in list:
            item = row[0]
            prices[item] = row[1]

    with open('ServiceDatesList.csv', 'r') as file:
        list = csv.reader(file)
        for row in list:
            item = row[0]
            serviceDate[item] = row[1]
    return manufact, prices, serviceDate

#Code for inputting and creating inventory items
def new_inventory(manufact, prices, serviceDate):
    inventory = []
    for item in manufact:
        item_data = manufact[item]
        price = prices.get(item)  
        service_date = serviceDate.get(item) 
        inventory.append({
            'item': item,
            'manufacturer': item_data['manufacturer'],
            'itemType': item_data['itemType'],
            'damaged': item_data['damaged'],
            'price': price,
            'service_date': service_date
        })
    return inventory

# Sorting functions
def sort_manufact(item):
    return item['manufacturer']
def sort_item(item):
    return item['item']
def sort_serviceDate(item):
    return new_date(item['service_date'])
def sort_price(item):
    return int(item['price'])

# Turning string into a data object
def new_date(format_date):
    return datetime.strptime(format_date, '%m/%d/%Y')  

# Turning date object to string and removing extra 0s
def format_date(date_format):
    if date_format:
        return f"{date_format.month}/{date_format.day}/{date_format.year}"
    return None

# Full Inventory code sorted by manufacterer name
def inventory_data(inventory):
    inventory.sort(key=sort_manufact)
    with open('FullInventory.csv', 'w', newline='') as file:
        object = csv.writer(file)
        for item in inventory:
            object.writerow([
                item['item'], 
                item['manufacturer'], 
                item['itemType'], 
                item['price'], 
                format_date(new_date(item['service_date'])), 
                item['damaged']
            ])

    # Code for Item types sorted by item type 
    itemTypes = {}
    for item in inventory:
        itemType = item['itemType']
        if itemType not in itemTypes:
            itemTypes[itemType] = []
        itemTypes[itemType].append(item)

    for itemType, items in itemTypes.items():
        items.sort(key=sort_item)  
        with open(f'{itemType}Inventory.csv', 'w', newline='') as file:
            object = csv.writer(file)
            for item in items:
                object.writerow([
                    item['item'], 
                    item['manufacturer'], 
                    item['price'], 
                    format_date(new_date(item['service_date'])), 
                    item['damaged']
                ])

    #Past service date code sorted by service date
    today = datetime.now()
    serviceItems = []
    for item in inventory:
        service_date = new_date(item['service_date'])
        if service_date and service_date < today:
            serviceItems.append(item)
    serviceItems.sort(key=sort_serviceDate)  
    with open('PastServiceDateInventory.csv', 'w', newline='') as file:
        object = csv.writer(file)
        for item in serviceItems:
            object.writerow([
                item['item'], 
                item['manufacturer'], 
                item['itemType'], 
                item['price'], 
                format_date(new_date(item['service_date'])), 
                item['damaged']
            ])

    # Damaged inventory items sorted by price code 
    damaged_items = [item for item in inventory if item['damaged']]
    damaged_items.sort(key=sort_price, reverse=True)
    with open('DamagedInventory.csv', 'w', newline='') as file:
        object = csv.writer(file)
        for item in damaged_items:
            object.writerow([
                item['item'], 
                item['manufacturer'], 
                item['itemType'], 
                item['price'], 
                format_date(new_date(item['service_date']))
            ])

# Main function 
def main():
    manufact, prices, serviceDate = import_data()
    inventory = new_inventory(manufact, prices, serviceDate)
    inventory_data(inventory)
if __name__ == "__main__":
    main()
