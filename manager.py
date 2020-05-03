import csv
from typing import Dict
from models import Mentee
from environment import *


# Create mentees from CSV file
def create_mentees() -> Dict[str, Mentee]:
    mentees = {}
    with open(MENTEE_CSV, encoding='utf-8') as mentee_file:
        reader = csv.DictReader(mentee_file)
        for row in reader:
            mentee_id = row[COLUMN_ID]
            mentee_name = row[COLUMN_NAME]
            if mentee_id == '' or mentee_name == '':
                print('Empty student record found. Please check the CSV file.')
                exit(1)
            mentees[mentee_id] = Mentee(mentee_id, mentee_name)
        return mentees


# Create result csv file
def create_result_csv(mentees: Dict[str, Mentee]):
    with open(RESULT_CSV, 'w', encoding='utf-8', newline='') as result_file:
        field_names = ['ID', 'name', 'file', 'score', 'note']
        writer = csv.DictWriter(result_file, fieldnames=field_names)
        writer.writeheader()
        for mentee in mentees.values():
            print()
            print('-' * 12, 'SUMMARY OF SUBMISSIONS', '-' * 12)
            mentee.print_submissions_summary()
            print('-' * 47)
            print()

            if mentee.submitted:
                for submission in mentee.submissions:
                    info = {
                        'ID': mentee.ID,
                        'name': mentee.name,
                        'file': submission.file_name,
                        'score': submission.score,
                        'note': submission.note
                    }
                    writer.writerow(info)
            else:
                info = {
                    'ID': mentee.ID,
                    'name': mentee.name,
                    'file': '',
                    'score': 0,
                    'note': 'NO SUBMISSION'
                }
                writer.writerow(info)

        result_file.close()
        # print_csv()

        return mentees


def print_csv():
    with open(RESULT_CSV, encoding='utf-8') as result_file:
        header_line = result_file.readline()
        for header in header_line.split(','):
            print(header.capitalize(), end='\t')
        print()

        for result in result_file.readlines():
            for data in result.split(','):
                print(data, end='\t')
            print()
        result_file.close()
