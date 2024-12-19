import os

from dotenv import load_dotenv
from terminaltables import SingleTable

from get_hh_sj_statistics import get_statistics_hh, get_statistic_sj


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



def main():
    load_dotenv()
    sj_key = os.getenv('SJ_SECRET_KEY')

    programming_languages = ['Python', 'Shell', 'C#', 'C++', 'Java', 'JavaScript', 'PHP', 'SQL', 'TypeScript']

    creste_statistic_table(statistic_vacancies=get_statistics_hh(programming_languages), title='HeadHunter Moscow')
    creste_statistic_table(statistic_vacancies=get_statistic_sj(programming_languages, sj_key), title='SuperJob Moscow')


if __name__ == '__main__':
    main()