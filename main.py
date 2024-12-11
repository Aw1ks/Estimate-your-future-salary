import requests
import os

from pprint import pprint
from itertools import count
from dotenv import load_dotenv


def get_vacancies_hh(programming_language):
    hh_link = 'https://api.hh.ru/vacancies'
    hh_payload = {
        "text": programming_language, 
        "area": 1
        }
    response_hh = requests.get(hh_link, params=hh_payload)
    response_hh.raise_for_status()
    hh_vacancies = response_hh.json()

    return hh_vacancies


def predict_rub_salary_hh(currency_vac, from_salary, to_salary):
    if currency_vac != 'RUR' or 'RUB':
        if from_salary and to_salary:
            average_salary = int((from_salary+to_salary)/2)
        elif from_salary:
            average_salary = int(from_salary*1.2)
        else:
            average_salary = int(to_salary*0.8)
    return average_salary


def statistic_hh():
    statistic_vacancies = {}
    programming_languages = ['Python', 'Shell', 'C#', 'C++', 'Java', 'JavaScript', 'Ruby', 'GO', '1C']

    for programming_language in programming_languages:
        all_salarys = []
        hh_vacancies = get_vacancies_hh(programming_language)

        for programmer_vacancy in hh_vacancies['items']:
                for page in count(0):
                    salary_prog = programmer_vacancy['salary']
                    if 'pages' in hh_vacancies:
                        if page >= hh_vacancies['pages'] -1:
                            break

                    if salary_prog != None:
                        currency_vac = salary_prog.get('currency')

                        from_salary = salary_prog['from']
                        to_salary = salary_prog['to']
                        average_salary = predict_rub_salary_hh(currency_vac, from_salary, to_salary)
                        all_salarys.append(average_salary)

        statistic_vacancies[programming_language] = {
            "vacancies_found": hh_vacancies['found'],
            "vacancies_processed": len(all_salarys),
            "average_salary": int(sum(all_salarys)/len(all_salarys))
        }
    pprint(statistic_vacancies)


statistic_hh()

