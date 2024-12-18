import os

from dotenv import load_dotenv
from terminaltables import SingleTable

from get_hh_sj_statistics import get_statistics_hh, get_statistic_sj, SJ_KEY, PROGRAMMING_LANGUAGES


def creste_statistic_table(statistic_vacancies, title):
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


if __name__ == '__main__':
    creste_statistic_table(statistic_vacancies=get_statistics_hh(PROGRAMMING_LANGUAGES), title='HeadHunter Moscow')
    creste_statistic_table(statistic_vacancies=get_statistic_sj(PROGRAMMING_LANGUAGES, SJ_KEY), title='SuperJob Moscow')