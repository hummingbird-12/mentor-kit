import csv
import os
from typing import Dict


class Mentee:
    ID: str
    name: str
    submitted: bool
    score: int
    note: str

    def __init__(self, _id: str, name: str):
        self.ID = _id
        self.name = name


COLUMN_ID = 'ID'
COLUMN_NAME = 'Name'
MENTEE_CSV = 'mentee.csv'
SUBMISSION_DIRECTORY_PATH = 'student-submissions'
mentees: Dict[str, Mentee] = {}

with open(MENTEE_CSV, encoding='utf-8') as menteeFile:
    reader = csv.DictReader(menteeFile)
    for row in reader:
        if row[COLUMN_ID] == '' or row[COLUMN_NAME] == '':
            print('Empty student record found. Please check the CSV file.')
            exit(1)
        mentees[row[COLUMN_ID]] = Mentee(row[COLUMN_ID], row[COLUMN_NAME])

submissionFiles = os.listdir(SUBMISSION_DIRECTORY_PATH)
for file in submissionFiles:
    dash = file.index('-')
    bracket = file.index(']')
    fileID = file[dash + 1:bracket]

    if fileID in mentees:
        mentees[fileID].submitted = True
    else:
        print("Deleting " + os.path.join(SUBMISSION_DIRECTORY_PATH, file))
        os.remove(os.path.join(SUBMISSION_DIRECTORY_PATH, file))

notSubmitted: [Mentee] = list(
    filter(lambda m: not m.submitted, mentees.values()))
if len(notSubmitted) == 0:
    print('Everybody submitted!')
else:
    print('Mentees not submitted:')
    for noSubmit in notSubmitted:
        print(noSubmit.name)
