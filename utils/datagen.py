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
import os, time, json, io, random, timeit, sys, datetime

class CartGenerator:

  def __init__(self, datasize, write_location):
    """
      Creates text files with cart data based on input size and write location
    """
    self.datasize = datasize
    self.write_location = write_location
    self.unix_timestamp = round(time.time(),2)
    self.db = []
    self.create_db()

    if (write_location is not None):
      self.output_type = '.txt'
      self.write_file()

  def create_db(self):
    """
      Create a list of 30 items (randomly to pick from in the future), only will run item generator 30 times
    """
    for x in range(30):
      item = self.random_item_generator(x)
      self.db.append(item)

  def random_item_generator(self, item_id):
    """
      Logic to create the items, will just create an item list
    """
    item_price = [round(random.uniform(1,100),2), round(random.uniform(150,250),2), round(random.uniform(250,600),2)]
    shipping_cost = round(random.uniform(5,10),2)

    return {
      "id": item_id,
      "shipping_cost": shipping_cost,
      "item_price": item_price[random.randint(0,2)],
      "valid_purchase": "False",
      "quantity": 0
    }

  def data_generation(self, cart_id):
    """
      Generates cart data based on datasize
    """

    data = {
      "id": cart_id,
      "user_id": random.randint(1,self.datasize),
      "shipping_cost": 0,
      "subtotal": 0,
      "item_list": []
    }

    counter = random.randint(1,3)
    subtotal = 0
    shipping_cost = 0

    for x in range(counter):
      item = self.db[random.randint(0,29)]
      item['quantity'] = random.randint(1,5)
      subtotal = item['quantity'] * item['item_price'] + subtotal
      shipping_cost = item['shipping_cost'] + shipping_cost
      data['item_list'].append(item)

    data['subtotal'] = round(subtotal,2)
    data['shipping_cost'] = round(shipping_cost,2)
  
    return data

  def write_file(self):
    """
      Write it to the location of execution, writes as a txt file
    """

    location = os.path.join(self.write_location,'Data'+str(self.unix_timestamp)+self.output_type)

    if self.datasize > 5000000:
      print('Input large, splitting to smaller files')
      remainder = self.datasize % 1000000
      counter = 0
      
      while counter < self.datasize:
        print(counter)
        with open(location, "w") as outfile:
          for x in range(1000000):
            temp_item = self.data_generation(x + counter)  
            json.dump(temp_item, outfile, ensure_ascii=False)
            outfile.write(",\n")
        outfile.close()
        counter = counter + 1000000

        location = os.path.join(self.write_location,'Data'+str(round(time.time(),2))+self.output_type)

      location = os.path.join(self.write_location,'Data'+str(round(time.time(),2))+self.output_type)
      with open(location, "w") as outfile:
        for x in range(remainder):
          temp_item = self.data_generation(x + counter)
          json.dump(temp_item, outfile, ensure_ascii=False)
          outfile.write(",\n")
    else:
      with open(location, "w") as outfile:
        for x in range(self.datasize):
          temp_item = self.data_generation(x)
          json.dump(temp_item, outfile, ensure_ascii=False)
          outfile.write(",\n")

if __name__ == "__main__":
  print(__name__)
  print(os.path.dirname(os.path.realpath(__file__)))
  start = datetime.datetime.now()
  CartGenerator(int(sys.argv[1]), os.path.dirname(os.path.realpath(__file__)))
  end = datetime.datetime.now()
  print(end - start)