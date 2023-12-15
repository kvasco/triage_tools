#!/bin/python2
##############################################################################
# todo - An example for JSON
##############################################################################

## >>> import json
## >>> import requests
## >>> response = requests.get("https://jsonplaceholder.typicode.com/todos")
## >>> todos = json.loads(response.text)
## >>> todos[:10]
## [{u'completed': False, u'userId': 1, u'id': 1, u'title': u'delectus aut autem'}, {u'completed': False, u'userId': 1, u'id': 2, u'title': u'quis ut nam facilis et officia qui'}, {u'completed': False, u'userId': 1, u'id': 3, u'title': u'fugiat veniam minus'}, {u'completed': True, u'userId': 1, u'id': 4, u'title': u'et porro tempora'}, {u'completed': False, u'userId': 1, u'id': 5, u'title': u'laboriosam mollitia et enim quasi adipisci quia provident illum'}, {u'completed': False, u'userId': 1, u'id': 6, u'title': u'qui ullam ratione quibusdam voluptatem quia omnis'}, {u'completed': False, u'userId': 1, u'id': 7, u'title': u'illo expedita consequatur quia in'}, {u'completed': True, u'userId': 1, u'id': 8, u'title': u'quo adipisci enim quam ut ab'}, {u'completed': False, u'userId': 1, u'id': 9, u'title': u'molestiae perspiciatis ipsa'}, {u'completed': True, u'userId': 1, u'id': 10, u'title': u'illo est ratione doloremque quia maiores aut'}]


import json

# not available for python3 at CN
#import requests

# for python3 try
#import got

# #response = requests.get("https://jsonplaceholder.typicode.com/todos")
#  
# #todos = json.loads(response.text)
#  
# # Write raw TODOs to file.
# with open("todo_data_file.json", "w") as data_file:
#     json.dump(todos, data_file, indent=2)

with open('todo_data_file.json') as file_object:
     todos = json.load(file_object)


#print("The variable todos is of type: ", type(todos))
# Print first 10 items in list todos
#print(todos[:10])

# Sample item from todos
# {
#     "userId": 1,
#     "id": 1,
#     "title": "delectus aut autem",
#     "completed": false
# }


# Map of userId to number of complete TODOs for that user
todos_by_user = {}

# Increment complete TODOs count for each user.
for todo in todos:
    if todo["completed"]:
        try:
            # Increment the existing user's count.
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            # This user has not been seen. Set their count to 1.
            todos_by_user[todo["userId"]] = 1

# Create a sorted list of (userId, num_complete) pairs.
top_users = sorted(todos_by_user.items(), 
                   key=lambda x: x[1], reverse=True)

# Get the maximum number of complete TODOs.
max_complete = top_users[0][1]

# Create a list of all users who have completed
# the maximum number of TODOs.
users = []
for user, num_complete in top_users:
    if num_complete < max_complete:
        break
    users.append(str(user))

max_users = " and ".join(users)

print("max_complete = ", max_complete)
print("max_users = ", max_users)

s = "s" if len(users) > 1 else ""
# This is python3 style printing. Not compatible with python2
#print(f"user{s} {max_users} completed {max_complete} TODOs")

#################################################################################
 
# Define a function to filter out completed TODOs 
# of users with max completed TODOS.
def keep(todo):
    is_complete = todo["completed"]
    has_max_count = str(todo["userId"]) in users
    return is_complete and has_max_count
 
# Write filtered TODOs to file.
with open("todo__filtered_data_file.json", "w") as data_file:
    filtered_todos = list(filter(keep, todos))
    json.dump(filtered_todos, data_file, indent=2)

