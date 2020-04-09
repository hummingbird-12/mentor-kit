import os
from typing import Dict
from Mentee import Mentee
from environment import *


# Filter out files not corresponding to the mentees
def filter_files(mentees: Dict[str, Mentee]) -> [str]:
    submission_files = os.listdir(SUBMISSION_DIRECTORY_PATH)
    for file in submission_files:
        dash = file.index('-')
        bracket = file.index(']')
        file_id = file[dash + 1:bracket]
        full_path = os.path.join(SUBMISSION_DIRECTORY_PATH, file)

        if file_id in mentees:
            mentees[file_id].assign_submission(full_path)
        else:
            print("Deleting " + full_path)
            os.remove(full_path)
    return os.listdir(SUBMISSION_DIRECTORY_PATH)


# List mentees who did not submit
def print_submission_result(mentees: Dict[str, Mentee]) -> None:
    not_submitted: [Mentee] = list(
        filter(lambda m: not m.submitted, mentees.values()))
    if len(not_submitted) == 0:
        print('Everybody submitted!')
    else:
        print('Mentees not submitted:')
        for noSubmit in not_submitted:
            print(noSubmit.name)
