import csv
from typing import Dict
from Mentee import Mentee
from environment import *


# Create mentees from CSV file
def create_mentees() -> Dict[str, Mentee]:
    mentees: Dict[str, Mentee] = {}
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
    with open(RESULT_CSV, 'w', encoding='utf-8') as result_file:
        field_names = ['ID', 'name', 'score', 'note']
        writer = csv.DictWriter(result_file, fieldnames=field_names)
        writer.writeheader()
        for mentee in mentees.values():
            mentee.print_submission_summary()
            info = {}
            for field in field_names:
                info[field] = mentee.__getattribute__(field)
            writer.writerow(info)
        return mentees
