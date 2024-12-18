# Estimate-your-future-salary
This project takes vacancies in certain programming languages with the Superjob API and the HeadHunter API and then turns the data into a table.
## How to install
This project uses libraries such as:[os](https://docs.python.org/3/library/os.html), [dotenv](https://betterdatascience-page.pages.dev/python-dotenv/), [requests](https://python-scripts.com/requests?ysclid=lyr2i4f3us982315000), [terminaltables](https://pypi.org/project/terminaltables/) and [itertools](https://docs.python.org/3/library/itertools.html).

The API key is only used for SuperJob, and you can get it on the official [website](https://api.superjob.ru/).

Python3 should already be installed. Use `pip` (or `pip3`, there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To save the data from prying eyes, we will create an .env file in which we will place: Sj_Secret_key.
Let's do it this way: 
```
SJ_SECRET_KEY = 'the secret key that you received'
```
## Environment variables
Environment variables are key—value pairs that determine the settings and behavior of the operating system and programs. You can read more here [More about Environment Variables] (https://habr.com/ru/companies/gnivc/articles/792082 /)

The launch_id variable takes the SuperJob API key from the file.env using the [os] library(https://docs.python.org/3/library/os.html ) using the `.getenv` method:
```
SJ_KEY = os.getenv('SJ_SECRET_KEY')
```
## How to launch
To run the script, you need to enter it into the console according to this example:
```
python crate_table_hh_and_sj.py
```
