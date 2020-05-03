import os
from shutil import copyfile
from typing import Dict
from models import Mentee
from environment import *
import sys


def cleanup_files():
    print('Deleting submission files...')
    submission_files = os.listdir(SUBMISSION_DIRECTORY)
    for file in submission_files:
        full_path = os.path.join(SUBMISSION_DIRECTORY, file)
        os.remove(full_path)

    print('Deleting output files...')
    output_files = os.listdir(OUTPUT_DIRECTORY)
    for file in output_files:
        full_path = os.path.join(OUTPUT_DIRECTORY, file)
        os.remove(full_path)

    print('Clean up complete!')


# Filter out files not corresponding to the mentees
def filter_files(mentees: Dict[str, Mentee]) -> [str]:
    submission_files = os.listdir(SUBMISSION_DIRECTORY)
    for file in submission_files:
        dash = file.index('-')
        bracket = file.index(']')
        file_id = file[dash + 1:bracket]
        file_name = file[1:dash]
        full_path = os.path.join(SUBMISSION_DIRECTORY, file)

        if file_id in mentees:
            if sys.platform == 'win32':
                delimiter = '\\'
            else:
                delimiter = '/'
            new_name = full_path.split(delimiter)[-1]
            new_name = '[{}-{}]{}'.format(file_id, file_name,
                                          new_name.split(']')[-1])
            path = full_path.split(delimiter)[:-1]
            path.append(new_name)
            new_path = delimiter.join(path)
            copyfile(full_path, new_path)
            mentees[file_id].assign_submission(new_path)
        else:
            print("Deleting " + full_path)
            os.remove(full_path)
    return os.listdir(SUBMISSION_DIRECTORY)


# List mentees who did not submit
def print_filtering_result(mentees: Dict[str, Mentee]) -> None:
    not_submitted = list(
        filter(lambda m: not m.submitted, mentees.values()))
    if len(not_submitted) == 0:
        print('Everybody submitted!')
    else:
        print('Mentees not submitted:')
        for noSubmit in not_submitted:
            print(noSubmit.name)
