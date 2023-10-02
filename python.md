JSON is the main format for sending and receiving data through APIs.

Python offers great support for JSON through its `json` library. We can convert lists and dictionaries to JSON, and vice versa.

The JSON library has two main methods:
  `dumps` - takes in a Python object and converts it to a string
  `loads` - takes in a JSON string and converts it to a Python object

Example:

import json
# Make a list of fast food chains.
best_food_chains = ["Taco Bell", "Shake Shack", "Chipotle"]
print(type(best_food_chains))

# Import the JSON library.
import json

# Use json.dumps to convert best_food_chains to a string.
best_food_chains_string = json.dumps(best_food_chains)
print(type(best_food_chains_string))

# Convert best_food_chains_string back to a list.
print(type(json.loads(best_food_chains_string)))

# Make a dictionary
fast_food_franchise = {
    "Subway": 24722,
    "McDonalds": 14098,
    "Starbucks": 10821,
    "Pizza Hut": 7600
}

# We can also dump a dictionary to a string and load it.
fast_food_franchise_string = json.dumps(fast_food_franchise)
print(type(fast_food_franchise_string))

fast_food_franchise_2 = json.loads(fast_food_franchise_string)
print(type(fast_food_franchise_2))

Output:

<class 'list'> </br>
<class 'str'> </br>
<class 'list'> </br>
<class 'str'> </br>
<class 'dict'> </br>

The server sends more than a status code and the data when it generates a response. It also sends metadata with information on how it generated the data and how to decode it. This information appears in the response headers. We can access it using the .headers property

print(response.headers)

convert response to json - response.json()

