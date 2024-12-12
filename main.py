import requests
import os

from pprint import pprint
from itertools import count
from dotenv import load_dotenv


def get_vacancies_hh(programming_language, hh_link):
    hh_payload = {
        "text": programming_language, 
        "area": 1
        }
    response_hh = requests.get(hh_link, params=hh_payload)
    response_hh.raise_for_status()
    hh_vacancies = response_hh.json()

    return hh_vacancies


def predict_rub_salary_hh(currency_vac_hh, from_salary_hh, to_salary_hh):
    if currency_vac_hh != 'RUR' or 'RUB':
        if from_salary_hh and to_salary_hh:
            average_salary_hh = int((from_salary_hh+to_salary_hh)/2)
        elif from_salary_hh:
            average_salary_hh = int(from_salary_hh*1.2)
        else:
            average_salary_hh = int(to_salary_hh*0.8)
    return average_salary_hh


def statistic_hh(programming_languages, hh_link):
    statistic_vacancies_hh = {}

    for programming_language in programming_languages:
        all_salarys_hh = []
        hh_vacancies = get_vacancies_hh(programming_language, hh_link)

        for programmer_vacancy_hh in hh_vacancies['items']:
                for page in count(0):
                    if 'pages' in hh_vacancies:
                        if page >= hh_vacancies['pages'] - 1:
                            break

                    salary_programming_hh = programmer_vacancy_hh['salary']
                    if salary_programming_hh != None:
                        currency_vac_hh = salary_programming_hh.get('currency')
                        from_salary_hh = salary_programming_hh['from']
                        to_salary_hh = salary_programming_hh['to']
                        hh_average_salary = predict_rub_salary_hh(currency_vac_hh, from_salary_hh, to_salary_hh)
                        all_salarys_hh.append(hh_average_salary)

        statistic_vacancies_hh[programming_language] = {
            "hh_vacancies_found": hh_vacancies['found'],
            "hh_vacancies_processed": len(all_salarys_hh),
            "hh_average_salary": int(sum(all_salarys_hh)/len(all_salarys_hh))
        }
    pprint(statistic_vacancies_hh)


def get_vacancies_sj(programming_language, sj_key, sj_link):
    sj_payload = {
        'period': 0,
        'town': 4,
        'keyword': programming_language,
        'app_key': sj_key
    }
    response_sj = requests.get(sj_link, params=sj_payload)
    response_sj.raise_for_status()
    sj_vacancies = response_sj.json()

    return sj_vacancies


def predict_rub_salary_sj(currency_vac_sj, from_sj_salary, to_sj_salary):
    if currency_vac_sj == 'rub':
        if from_sj_salary and to_sj_salary:
            average_salary_sj = int((from_sj_salary+to_sj_salary)/2)
        elif from_sj_salary:
            average_salary_sj = int(from_sj_salary*1.2)
        else:
            average_salary_sj = int(to_sj_salary*0.8)
    return average_salary_sj


def statistic_sj(programming_languages, sj_key, sj_link):
    statistic_vacancies_sj = {}

    for programming_language in programming_languages:
        all_salarys_sj = []
        sj_vacancies = get_vacancies_sj(programming_language, sj_key, sj_link)

        for sj_professions in sj_vacancies['objects']:
            for page in count(0):
                if page >= len(sj_vacancies):
                    break

                currency_vac_sj = sj_professions.get('currency')
                from_sj_salary = sj_professions['payment_from']
                to_sj_salary = sj_professions['payment_to']
                sj_average_salary = predict_rub_salary_sj(currency_vac_sj, from_sj_salary, to_sj_salary)
                all_salarys_sj.append(sj_average_salary)

            statistic_vacancies_sj[programming_language] = {
                    "sj_vacancies_found": len(sj_vacancies),
                    "sj_vacancies_processed": len(all_salarys_sj),
                    "sj_average_salary": int(sum(all_salarys_sj)/len(all_salarys_sj))
                }
    pprint(statistic_vacancies_sj)


def main():
    load_dotenv()
    sj_key = os.getenv('Sj_Secret_key')

    programming_languages = ['Python', 'Shell', 'C#', 'C++', 'Java', 'JavaScript', 'Ruby', 'GO', '1C']
    hh_link = 'https://api.hh.ru/vacancies'
    sj_link = 'https://api.superjob.ru/2.0/vacancies/'

    statistic_hh(programming_languages, hh_link)
    statistic_sj(programming_languages, sj_key, sj_link)


if __name__ == '__main__':
    main()