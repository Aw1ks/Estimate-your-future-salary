import requests
import os

from itertools import count
from dotenv import load_dotenv
from terminaltables import SingleTable


def get_vacancies_hh(programming_language, page=0):
    hh_link = 'https://api.hh.ru/vacancies'
    moscow_area = 1

    hh_payload = {
        "text": programming_language, 
        "area": moscow_area,
        "page": page
    }
    response_hh = requests.get(hh_link, params=hh_payload)
    response_hh.raise_for_status()
    hh_vacancies = response_hh.json()
    return hh_vacancies


def get_vacancies_sj(programming_language, sj_key, page):
    sj_link = 'https://api.superjob.ru/2.0/vacancies/'
    publication_period = 0
    moscow_town = 4

    sj_payload = {
        'period': publication_period,
        'town': moscow_town,
        'keyword': programming_language,
        'app_key': sj_key,
        'page': page
    }
    response_sj = requests.get(sj_link, params=sj_payload)
    response_sj.raise_for_status()
    sj_vacancies = response_sj.json()
    return sj_vacancies


def predict_rub_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        average_salary = int((salary_to + salary_from) / 2)
    elif salary_to:
        average_salary = int(salary_to * 1.2)
    elif salary_from:
        average_salary = int(salary_from * 0.8)
    else:
        average_salary = None
    return average_salary


def get_statistics_hh(programming_languages):
    vacancies_statistic = {}

    for programming_language in programming_languages:
        all_salary_hh = []

        for page in count(0):
            hh_vacancies = get_vacancies_hh(programming_language, page=0)

            if 'pages' in hh_vacancies:
                if page >= hh_vacancies['pages'] - 1:
                    break
            for vacancy_hh in hh_vacancies['items']:
                salary_vacancy_hh = vacancy_hh['salary']
                if salary_vacancy_hh:
                    currency_vac_hh = salary_vacancy_hh.get('currency')

                    if currency_vac_hh != 'RUR' or 'RUB':
                        hh_average_salary = predict_rub_salary(salary_from=salary_vacancy_hh['from'], salary_to=salary_vacancy_hh['to'])
                        all_salary_hh.append(hh_average_salary)

        average_salary = None
        if all_salary_hh:
            average_salary = int(sum(all_salary_hh) / len(all_salary_hh))

        vacancies_statistic[programming_language] = {
            "vacancies_found": hh_vacancies['found'],
            "vacancies_processed": len(all_salary_hh),
            "average_salary": average_salary
        }
    return vacancies_statistic


def get_statistic_sj(programming_languages, sj_key):
    vacancies_statistic = {}

    for programming_language in programming_languages:
        salary_vacancies = []

        for page in count(0, 1):
            sj_vacancies = get_vacancies_sj(programming_language, sj_key, page=page)
            total_vacancies = sj_vacancies['total']

            if not sj_vacancies['objects']:
                break

            for sj_vacancy in sj_vacancies['objects']:
                currency_vac_sj = sj_vacancy.get('currency')

                if currency_vac_sj != 'RUR' or 'RUB':
                    sj_average_salary = predict_rub_salary(salary_from=sj_vacancy['payment_from'], salary_to=sj_vacancy['payment_to'])

                    if sj_average_salary:
                        salary_vacancies.append(sj_average_salary)

        average_salary = None
        if salary_vacancies:
            average_salary = int(sum(salary_vacancies) / len(salary_vacancies))
            
        vacancies_statistic[programming_language] = {
            'vacancies_found': total_vacancies,
            'vacancies_processed': len(salary_vacancies),
            'average_salary': average_salary
        }
    return vacancies_statistic


def create_statistic_table(statistic_vacancies, title):
    table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]

    for programming_language, vacancies_key in statistic_vacancies.items():
        table.append([
            programming_language,
            vacancies_key['vacancies_found'],
            vacancies_key['vacancies_processed'],
            vacancies_key['average_salary']
        ])
    statistic_table = SingleTable(table, title)
    print(statistic_table.table)


def main():
    load_dotenv()
    sj_key = os.getenv('SJ_SECRET_KEY')

    programming_languages = ['Python', 'Shell', 'C#', 'C++', 'Java', 'JavaScript', 'PHP', 'SQL', 'TypeScript']

    create_statistic_table(statistic_vacancies=get_statistics_hh(programming_languages), title='HeadHunter Moscow')
    create_statistic_table(statistic_vacancies=get_statistic_sj(programming_languages, sj_key), title='SuperJob Moscow')


if __name__ == '__main__':
    main()