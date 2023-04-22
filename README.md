# CENG 495 - 2023 - HW1

Register: https://ceng495-hw1.onrender.com/auth
Login: https://ceng495-hw1.onrender.com/auth

Admin Login: 
username: admin
password: admin123

Create Item: https://ceng495-hw1.onrender.com/create_item
-Name
-Price (float)
-Category
-Description
-Seller
-Size
Optional Fields:
-Image Url
-Color
-Spec

Delete Item:
Choose Item from main page, click "Delete Item" in the bottom of item page.

Update Item:
Choose Item from main page, make desired changes in page click "Save Changes" in the bottom of item page.

Delete User: https://ceng495-hw1.onrender.com/users
Create User: https://ceng495-hw1.onrender.com/users

User Login:
username: ismail
password: ismail123

Add Review & Rate:
Choose Item from main page, click "Reviews" in the bottom of item page. Fill review form and click "Submit Review"

Why i used Flask?
Flask is a lightweight web framework that is well-suited for building small apps. Also in my work i was using Flask+MongoDB which i found very effective and the same time flexible. Also python based frameworks has Pydantic library which i strongly suggest while using MongoDB. Since MongoDB is NoSQL, validation must be done in before the database. Else its too hard to maintain consistent data and validate them. Except this thing since homework implies front-end side is not evaluated, i go on html which can be easily manipulated with Flask's Jinja2 library.

Directory Structure:

|____requirements.txt
|____custom_errors.py
|____models
| |____base_queries.py
| |____user
| | |____queries.py
| | |____base.py
| |____item
| | |____queries.py
| | |____base.py
| |____review
| | |____queries.py
| | |____base.py
| |____helpers.py
| |____create_collections.py

"models" directory is contains pydantic base models and mongo queries. Using Pydantic BaseModel with MongoDB makes it easier to define and validate data models with type hints, reducing the chances of errors. It also has native support for parsing and serializing MongoDB documents, making it a convenient choice for working with MongoDB.

|____README.md
|____.gitignore
|____app.py
|____templates
| |____index.html
| |____auth.html
| |____create_item.html
| |____users.html
| |____reviews.html
| |____item.html
|____modules
| |____controller.py
| |____auth
| | |____auth.py
| | |______init__.py
| | |____helpers.py
| | |____schema.py
| |____constants.py
| |______init__.py
| |____commons.py
| |____schema.py

schema.py is used to validate request parameters & json body. If request has errors, before creating base model we identify it.
controller.py and auth.py contains endpoints.
 
