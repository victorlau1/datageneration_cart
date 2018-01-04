"""
SCHEMA
{
  "id": 49100,
  "user_id": 23,
  "shipping_cost": 7.60,
  "subtotal": 148.00,
  "item_list": [{
        "id": 49200,
        "shipping_cost": 9.86,
        "item_price": 100.00,
        "valid_purchase": "False",
        "quantity": 3
        },
        {
        "id": 49100,
        "shipping_cost": 5.00,
        "item_price": 40.00,
        "valid_purchase":"False",
        "quantity": 2
        }]
}
"""
import os, time, json, io, random

class CartGenerator:

  def __init__(self, datasize, write_location):
    self.datasize = datasize
    self.write_location = write_location
    self.unix_timestamp = time.time()
    self.db = []
    self.create_db()
    self.write_file()

  def create_db(self):
    for x in range(30):
      item = self.random_item_generator(x)
      self.db.append(item)

  def random_item_generator(self, item_id):
    item_price = [random.uniform(1,100), random.uniform(150,250), random.uniform(250,600)]
    shipping_cost = random.uniform(5,10)

    return {
      "id": item_id,
      "shipping_cost": shipping_cost,
      "item_price": item_price[random.randint(0,2)],
      "valid_purchase": "False",
      "quantity": 0
    }

  def data_generation(self, cart_id):
    """
    Generates data based on datasize
    """

    data = {
      "id": cart_id,
      "user_id": random.randint(1,self.datasize),
      "shipping_cost": 0,
      "subtotal": 0,
      "item_list": []
    }

    counter = random.randint(1,5)

    for x in range(counter):
      item = self.db[random.randint(0,29)]
      subtotal = 0
      shipping_cost = 0
      item['quantity'] = random.randint(1,5)
      subtotal = item['quantity'] * item['item_price']
      shipping_cost = item['shipping_cost'] + shipping_cost
      data['item_list'].append(item)
      data['subtotal'] = subtotal
      data['shipping_cost'] = shipping_cost
  
    return data

  def write_file(self):
    
    location = os.path.join(self.write_location,'Data'+str(self.unix_timestamp)+'.json')
    print(location)
    with open(location, "w") as outfile:
      for x in range(self.datasize):
        json.dump(self.data_generation(self.datasize), outfile, ensure_ascii=False)  

print(os.path.dirname(os.path.realpath(__file__)))
CartGenerator(100, os.path.dirname(os.path.realpath(__file__)))