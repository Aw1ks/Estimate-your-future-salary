import requests
from pprint import pprint
from itertools import count


def get_vacancies(programming_language):
    all_vacancies = []
    for page in count(0):
        url = 'https://api.hh.ru/vacancies'
        payload = {"text": programming_language, "area": 1}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        vacancies = response.json()

        pprint(vacancies)

        if 'pages' in vacancies:
            if page >= vacancies["pages"] - 1:
                break
        return vacancies


def predict_rub_salary(currency_vac, from_salary, to_salary):
    if currency_vac != 'RUR' or 'RUB':
        if from_salary and to_salary:
            average_salary = int((from_salary+to_salary)/2)
        elif from_salary:
            average_salary = int(from_salary*1.2)
        else:
            average_salary = int(to_salary*0.8)
    return average_salary


def statistic_hh():
    vacancies = {}
    programming_languages = ['Python', ' C ', 'C#', 'C++', 'Java', 'JavaScript', 'Ruby', 'GO', '1C']

    for programming_language in programming_languages:
        all_salarys = []

        vacancies = get_vacancies(programming_language)
        for programmer_vacancy in vacancies['items']:
            salary_prog = programmer_vacancy['salary']

            if salary_prog != None:
                currency_vac = salary_prog.get('currency')

                from_salary = salary_prog['from']
                to_salary = salary_prog['to']
                average_salary = predict_rub_salary(currency_vac, from_salary, to_salary)
                all_salarys.append(average_salary)

        vacancies[programming_language] = {
            "vacancies_found": vacancies['found'],
            "vacancies_processed": len(all_salarys),
            "average_salary": int(sum(all_salarys)/len(all_salarys))
        }
    pprint(vacancies)
statistic_hh()