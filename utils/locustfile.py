from locust import HttpLocust, TaskSet
from datagen import CartGenerator
from random import randint
import json
from io import StringIO

def checkout(locust):
  url = '/purchases/'
  counter = randint(1,10000000)
  dataGenerator = CartGenerator(100, None)
  data = dataGenerator.data_generation(counter)
  io = StringIO()
  json.dump(data, io)
  locust.client.post(url, io.getvalue())
  counter = counter + 1

class UserBehavior(TaskSet):
  tasks = {checkout: 1}

  def on_start(self):
    checkout(self)

class WebsiteUser(HttpLocust):
  task_set = UserBehavior
  host = "http://localhost:8000"
  min_wait = 5000
  max_wait = 9000
