import requests
import os

from itertools import count
from dotenv import load_dotenv
from terminaltables import SingleTable


def get_vacancies_HH(programming_language, HH_link):
    HH_payload = {
        "text": programming_language, 
        "area": 1
        }
    response_HH = requests.get(HH_link, params=HH_payload)
    response_HH.raise_for_status()
    HH_vacancies = response_HH.json()
    return HH_vacancies


def predict_rub_salary_HH(currency_vac_HH, from_salary_HH, to_salary_HH):
    if currency_vac_HH != 'RUR' or 'RUB':
        if from_salary_HH and to_salary_HH:
            average_salary_HH = int((from_salary_HH+to_salary_HH)/2)
        elif from_salary_HH:
            average_salary_HH = int(from_salary_HH*1.2)
        else:
            average_salary_HH = int(to_salary_HH*0.8)
    return average_salary_HH


def statistic_HH(programming_languages, HH_link):
    statistic_vacancies_HH = {}

    for programming_language in programming_languages:
        all_salarys_HH = []
        HH_vacancies = get_vacancies_HH(programming_language, HH_link)

        for programmer_vacancy_HH in HH_vacancies['items']:
                for page in count(0):
                    if 'pages' in HH_vacancies:
                        if page >= HH_vacancies['pages'] - 1:
                            break

                    salary_programming_HH = programmer_vacancy_HH['salary']
                    if salary_programming_HH != None:
                        currency_vac_HH = salary_programming_HH.get('currency')
                        from_salary_HH = salary_programming_HH['from']
                        to_salary_HH = salary_programming_HH['to']
                        HH_average_salary = predict_rub_salary_HH(currency_vac_HH, from_salary_HH, to_salary_HH)
                        all_salarys_HH.append(HH_average_salary)

        statistic_vacancies_HH[programming_language] = {
            "HH_vacancies_found": HH_vacancies['found'],
            "HH_vacancies_processed": len(all_salarys_HH),
            "HH_average_salary": int(sum(all_salarys_HH) / len(all_salarys_HH))
        }
    return statistic_vacancies_HH


def HH_table(statistic_vacancies_HH):
    TABLE_HH = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for programming_language, HH_vacancies_key in statistic_vacancies_HH.items():
        TABLE_HH.append([
            programming_language,
            HH_vacancies_key['HH_vacancies_found'],
            HH_vacancies_key['HH_vacancies_processed'],
            HH_vacancies_key['HH_average_salary']
        ])
    HH_table_vacancies = SingleTable(TABLE_HH)
    HH_table_vacancies.title = 'HeadHunter Moscow'
    print(HH_table_vacancies.table)


def get_vacancies_SJ(programming_language, SJ_key, SJ_link, page):
    SJ_payload = {
        'period': 0,
        'town': 4,
        'keyword': programming_language,
        'app_key': SJ_key,
        'page': page
    }

    response_SJ = requests.get(SJ_link, params=SJ_payload)
    response_SJ.raise_for_status()
    SJ_vacancies = response_SJ.json()
    return SJ_vacancies


def predict_rub_salary_SJ(currency_vac_SJ, from_SJ_salary, to_SJ_salary):
    if currency_vac_SJ == 'rub':
        if from_SJ_salary and to_SJ_salary:
            average_salary_SJ = int((from_SJ_salary + to_SJ_salary) / 2)
        elif from_SJ_salary:
            average_salary_SJ = int(from_SJ_salary * 1.2)
        elif to_SJ_salary:
            average_salary_SJ = int(to_SJ_salary * 0.8)
        else:
            average_salary_SJ = None
    else:
        average_salary_SJ = None
    return average_salary_SJ


def statistic_SJ(programming_languages, SJ_key, SJ_link):
    vacancies_by_language = {}

    for programming_language in programming_languages:
        salary_vacancies = []

        for page in count(0):
            SJ_vacancies = get_vacancies_SJ(programming_language, SJ_key, SJ_link, page=page)
            total_vacancies = SJ_vacancies['total']

            if not SJ_vacancies['objects']:
                break

            for SJ_vacancy in SJ_vacancies['objects']:
                currency_vac_SJ = SJ_vacancy.get('currency')
                from_SJ_salary = SJ_vacancy['payment_from']
                to_SJ_salary = SJ_vacancy['payment_to']

                if from_SJ_salary or to_SJ_salary:
                    SJ_average_salary = predict_rub_salary_SJ(currency_vac_SJ, from_SJ_salary, to_SJ_salary)

                    if SJ_average_salary != None:
                        salary_vacancies.append(SJ_average_salary)

        average_salary = None
        if salary_vacancies:
            average_salary = int(sum(salary_vacancies) / len(salary_vacancies))
            
        vacancies_by_language[programming_language] = {
            'SJ_vacancies_found': total_vacancies,
            'SJ_vacancies_processed': len(salary_vacancies),
            'SJ_average_salary': average_salary
        }
    return vacancies_by_language


def SJ_table(statistic_vacancies_SJ):
    TABLE_SJ = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]

    for programming_language, SJ_vacancies_key in statistic_vacancies_SJ.items():
        TABLE_SJ.append([
            programming_language,
            SJ_vacancies_key['SJ_vacancies_found'],
            SJ_vacancies_key['SJ_vacancies_processed'],
            SJ_vacancies_key['SJ_average_salary']
        ])

    SJ_table_vacancies = SingleTable(TABLE_SJ)
    SJ_table_vacancies.title = 'SuperJob Moscow'
    print(SJ_table_vacancies.table)


def main():
    load_dotenv()
    SJ_key = os.getenv('SJ_Secret_key')

    programming_languages = ['Python', 'Shell', 'C#', 'C++', 'Java', 'JavaScript', 'PHP', 'SQL', 'TypeScript']
    HH_link = 'https://api.HH.ru/vacancies'
    SJ_link = 'https://api.superjob.ru/2.0/vacancies/'
    
    statistic_vacancies_HH = statistic_HH(programming_languages, HH_link)
    statistic_vacancies_SJ = statistic_SJ(programming_languages, SJ_key, SJ_link)

    HH_table(statistic_vacancies_HH)
    SJ_table(statistic_vacancies_SJ)


if __name__ == '__main__':
    main()