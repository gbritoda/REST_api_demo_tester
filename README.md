# REST API Tester

This repo was created as a solution for the following challenge:
[REST API Demo](https://github.com/amaccormack-lumira/rest_api_demo/blob/master/README.md) v1.2

## Recommendations after testing

### Fix dependency issue on API
**Werkzeug 0.16.1** is not compatible with the most current version of Flask. But updating Werkzeug will cause **flask-restplus** to not work. The community switched to **flask-restx** as **flask-restplus** lacked sufficient support. 

I recommend two options:

* Switch to **flask-restx** for a proper fix, but that could prove changing a lot of the code
* Add **Flask==1.1.1** to the dependencies (What I did). Fixing a compatible version of Flask

For the latter, please check my changes to:
* ./rest_api_demo-techtest1.2/requirements.txt
* ./rest_api_demo-techtest1.2/setup.py
### Bugs found
#### Category name missing first letter
When POSTING a new category, the name will miss the first letter

#### Blog Posts won't update past the first page
Out of the scope as this endpoint wasn't supposed to be tested, but I found it manually and decided to add it.
When using GET Blog posts you can't go past the first page.

## Getting started
The API was not functioning from the start due to Python dependency issues. I added a quick fix to it and it is also on this repo, inside the [rest_api_demo-techtest1.2](./rest_api_demo-techtest1.2) folder.

## Database folder
If you choose to use the API from this Repo, everything is already configured. If not, please change **database_path** on [config.json](./config.json) to the **db.sqlite** file of your API instalation. Also ensure you have writing permission to the same folder.

> This is because the test resets the database to a default stage by copying the database from the [default_database](./default_database) folder.

## Python requirements

> This application requires **Python 3.6+**
> To install the requirements **pip** is necessary

It is highly recommended to set up a virtual environment before.

To install the requirements simply call

```
pip install -r requirements.txt
```

The requirements are:
* **PyTest** for testing
* **requests** for interacting with HTTP protocol
* **colorama**, **pytest-html** and **ansi2html** for a colourful report

## Running the Test suite

* On Linux

```
./run_test.sh
```

* On Windows 8+ (Not tested!)
> Windows PowerShell is required
```
./run_test.ps1
```

* Any command line

```
py.test test_REST_API.py -v --html=report.html --self-contained-html 
```

## Tests

#### Reset database to default

Rewrites the db.sqlite file to a default stage

#### GET Blog categories
* Sends a GET request for /api/blog/categories
* Checks HTTP response code
* Checks if 'id', and 'name' are in the response
* Checks if there is nothing else in the response

#### POST, GET, and DELETE Blog Categories
* Posts a blog category
* Check if it was posted using GET
  * endpoint: /blog/categories/
* Deletes it

3 test cases for category names:
* "Category name"
* "A category name that is quite longer"
* "Category@name-with1symbols."

#### POST, GET by id, and DELETE Blog Categories
Same as above but using GET for the following endpoint:
* /blog/categories/{id}



#### POST, DELETE and GET Blog categories
* Posts a blog category
* Deletes it
* Check if it was deleted using GET


3 test cases for category id and names:
* 4, "Category name"
* 5, "A category name that is quite longer"
* 6, "Category@name-with1symbols."

#### POST, PUT, GET and DELETE Blog categories
* Posts a blog category
* Updates it with PUT
* Check if it was properly updated with GET
* Deletes it

3 test cases for category id and names:
* 4, "Category name"
* 5, "A category name that is quite longer"
* 6, "Category@name-with1symbols."+
  
#### POST invalid id format
* Tries posting 100 invalid ids at random and checks they are rejected
  * Random ids will be random characters of random length
  * Excluding digits and ':'

#### POST invalid name format
* Tries posting 100 invalid 'name' format and checks if they are rejected
  * Random names will be random floats and integers
  
#### PUT invalid id format
* Tries updating 100 invalid ids at random and checks they are rejected
  * Random ids will be random characters of random length
  * Excluding digits and ':'

#### PUT invalid name format
* Tries updating 100 invalid 'name' format and checks if they are rejected
  * Random names will be random floats and integers

#### DELETE invalid id format
* Tries deleting 100 invalid ids at random and checks they are rejected
  * Random ids will be random characters of random length

#### Test Blog post GET
* Extra test just to cover one issue I found manually
* Tries to get posts with random 'page' and 'per_page' parameters
* Checks if the 'page' and 'per_page' numbers are consistent
* Checks if 'per_page' and 'pages' are mathematically consistent with 'total'