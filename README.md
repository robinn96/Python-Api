# Api Request With Python

The idea of this project its to demostrate how to do api requests with a library call Request and making use of unittest(unit testing framework) to create the test itself.

## Libraries that are used in the project.
- [Request](https://docs.python-requests.org/en/latest/)
- [Unittest](https://docs.python.org/3/library/unittest.html#module-unittest)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Allure- Pytest](https://docs.qameta.io/allure-report/frameworks/python/pytest)
- [Pytest](https://docs.pytest.org/en/7.0.x/)

## Installation and configuration

First you need to have installed python3 in your computer. 

```bash
brew install python
```

The following module is also used [venv](https://docs.python.org/3/library/venv.html).
The venv module provides support for creating lightweight “virtual environments” with their own site directories so we don’t install python libraries that will be installed for the purpose of this demostration in global python.




## Usage

First, go inside the project and enter the following command in the terminal to activate the virtual environment in order to make use of the python version this project uses. 

```bash
source venv/bin/activate
```

Once this has been done, proceed to enter this command in order to installed the libraries required to run this project: 

```bash
pip install -r requirements.txt
```
Also in the root of the project you will see an .env file with this information. The first one its the Api Url. The second one will contain the token for some endpoints that needs authorization. 

Check [here](https://airportgap.dev-tester.com/tokens/new) to know how to get it.
```bash
API_TOKEN=''
BASE_URL='https://airportgap.dev-tester.com/api/'
```

Now we are ready!

## Scripts

To run the test execute the following command once inside tests folder:

```bash
pytest airport_test.py -s -v        
```

####  Reporting

Allure-pytest and allure-python-commons packages are used to produce report data compatible with Allure 2. To enable Allure listener to collect results during the test execution simply add **--alluredir** option and provide path to the folder where results should be stored. E.g.:

```bash
pytest airport_test.py -s -v --alluredir=/tmp/allure_results
```

To see the actual report after your tests have finished, you need to use Allure commandline utility to generate report from the results.

```bash
allure serve /tmp/allure_results
```
This command will show you generated report in your default browser.



## Usage

Most important folder are authentication and tests. 

We can manage different kinds of authentication handled by Request library. More later we are going to consume some endpoints that require auth, with Bearer token more specific. So we need to create a custom class to deal with this kind of authentication. 

This logic its located in the authentication folder. 

The other folder called tests include the test file in which will be a series of test making use of different HTPP methods. 

If we go inside this file we can see some couple of things like the imports.

```python
import requests
import unittest
import allure
import os

from dotenv import load_dotenv

from authentication.auth_token import BearerAuth
```

- requests - its the library that we will use to make the http request.
- allure - reporting tool
- Dotenv - its imported to load an environment variable so it will not be burned into the code.
- We also import the class in which we handle the authentication


In this other section we create a subclass of **unittest.TestCase**. It provides a rich set of tools for constructing and running tests.

Then we load all the environment variables like the api token.

And then we can see a **setUpClass** class, this is a class that the unit test frameworks provide to set some configurations there before all the test starts running.

```python
class AirportApiTest(unittest.TestCase):
    # load env variables
    load_dotenv()

    @classmethod
    def setUpClass(cls):
        """Runs before each test case"""
        cls.BASE_URL = os.environ.get("BASE_URL")
        cls.AIRPORT_API_KEY = os.environ.get("API_TOKEN")
```

Below will be show part of each test logic, in specific the one about the api request. At the end you will have a general overview of how to use the different http methods with Request library.


### Get - Request

We can do a simple get request just calling request.get and passing the api url as parameter. And in the response variable the response object will be stored.
```python
  def test_get_airports(self):
        """Returns all airports, limited to 30 per page"""
        url = f'{self.BASE_URL}/airports'
        response = requests.get(url)
```

### Post - Request

We can do a simple post request just calling request.post and passing the api url as parameter and the payload which its a dictionary assigned to the data argument. In the response variable the response object will be stored.

```python
 def test_calculate_distance_between_airports(self):
        url = f'{self.BASE_URL}/airports/distance'
        payload = {"from": "KIX", "to": "SFO"}

        response = requests.post(url, data=payload)
```

### Authentication

Sometimes some endpoints require some kind of authentication, for this scenario its a bearer token. So first we create a payload dictionary with the information we want to send. Then in request.post parameters we can see url which its the api url, the payload assigned to data argument and the BearerAuth class including the api token.

```python
 def test_allows_user_save_and_delete_their_favorite_airports(self):
        # Check that a user can create a favorite airport.
        url = f'{self.BASE_URL}/favorites'
        payload = {"airport_id": "JFK", "note": "My usual layover when visiting family"}

        response = requests.post(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
```

### Put - Request
First we create a payload dictionary with the information we want to update.
Then we just all requests.put and assign the payload to data argument. 

```python
    def test_allows_user_save_and_delete_their_favorite_airports(self):
        # Check that a user can update the note of the created favorite.
        payload = {"note": 'My usual layover when visiting family and friends'}
        url = f'{self.BASE_URL}/favorites/{favorite_id}'

        response = requests.put(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
```

### Delete - Request
First we create a payload dictionary with the information we want to delete.
Then we just all requests.delete and assign the payload to data argument. 

```python
    def test_allows_user_save_and_delete_their_favorite_airports(self):  
        # Check that a user can delete the created favorite.
        response = requests.delete(url, data=payload, auth=BearerAuth(self.AIRPORT_API_KEY))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
