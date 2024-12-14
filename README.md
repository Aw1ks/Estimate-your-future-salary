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
Sj_Secret_key = 'the secret key that you received'
```
## Environment variables
Environment variables are key—value pairs that determine the settings and behavior of the operating system and programs. You can read more here [More about Environment Variables] (https://habr.com/ru/companies/gnivc/articles/792082 /)

The launch_id variable takes the SuperJob API key from the file.env using the [os] library(https://docs.python.org/3/library/os.html ) using the `.getenv` method:
```
SJ_key = os.getenv('SJ_Secret_key')
```
## How it works
### To begin with, 2 functions are created to get the right job references.
Function for HeadHunter:
```
get_vacancies_HH
```
Function for SuperJob:
```
get_vacancies_SJ
```
Here, with the help of the [requests](https://python-scripts.com/requests?ysclid=lyr2i4f3us982315000) library, links are created to get vacancies
### Next, functions are created to calculate the average salary.
Function for HeadHunter:
```
predict_rub_salary_HH
```
Function for SuperJob:
```
predict_rub_salary_SJ
```
These functions use conditional constructions to get the average salary from vacancies
### After that, functions are created to collect all the received data and create a dictionary with values for each programming language.
Function for HeadHunter:
```
statistic_HH
```
Function for SuperJob:
```
statistic_SJ
```
These functions are designed to collect all the information received and convert it into dictionaries with data for each programming language
### And the last 2 functions are designed to create tables based on the values obtained.
Function for HeadHunter:
```
HH_table
```
Function for SuperJob:
```
SJ_table
```
In these 2 functions, 2 tables are created using the [itertools](https://docs.python.org/3/library/itertools.html) library and created dictionaries (for programming languages).
