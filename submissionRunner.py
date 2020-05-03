import os.path
import subprocess
import sys
from typing import Dict
from models import Mentee
from environment import *


def prompt_with_options(prompt: str, options: [str] = None) -> str:
    if options is None:
        options = ['y', 'n']
    while True:
        char = input('{} ({}) '.format(prompt, '/'.join(options)))
        if char in options:
            return char
        choices = ','.join(options[:-1]) + ' and {}'.format(options[-1])
        print("Please select between {}.".format(choices))


def run_c_file(file: str):
    if not file.endswith('.c'):
        print('File {} is not a .c file!'.format(file))
        return

    if not os.path.isdir(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)

    with open('input.txt', encoding='utf-8') as input_file:
        file_name = file.rstrip('.c').split('/')[-1]
        output_file = '{}/{}.out'.format(OUTPUT_DIRECTORY, file_name)
        if sys.platform == 'win32':
            pass
        else:
            try:
                subprocess.run(['gcc', '-o', output_file, file])
                subprocess.run(output_file, stdin=input_file)
            except FileNotFoundError:
                print('Compile error has occurred')

        input_file.close()


def run_py_file(file: str):
    if not file.endswith('.py'):
        print('File {} is not a .py file!'.format(file))
        return

    with open('input.txt', encoding='utf-8') as input_file:
        if sys.platform == 'win32':
            subprocess.run(['python', file], stdin=input_file)
        else:
            subprocess.run(['python3', file], stdin=input_file)
        input_file.close()


def runner(mentees: Dict[str, Mentee]):
    with_submission = list(filter(lambda m: m.submitted, mentees.values()))

    for mentee in with_submission:
        for submission in mentee.submissions:
            options = ['run', 'code', 'evaluate']
            answer = 'run'
            while True:
                if answer == 'run':
                    file_extension = submission.file_extension
                    if file_extension is None:
                        print('File {} has no extension!'.format(
                            submission.file_name))
                        continue

                    print()
                    print('-' * 12, 'BEGINNING OF OUTPUT', '-' * 12)
                    if file_extension == '.c':
                        run_c_file(submission.file)
                    elif file_extension == '.py':
                        run_py_file(submission.file)
                    else:
                        print('Extension .{} is not yet supported!'.format(
                            file_extension))
                    print('-' * 12, 'END OF OUTPUT', '-' * 12)
                    print()
                if answer == 'code':
                    print()
                    print('-' * 12, 'BEGINNING OF CODE', '-' * 12)
                    submission.print_file_content()
                    print('-' * 12, 'END OF CODE', '-' * 12)
                    print()
                if answer == 'evaluate':
                    break

                mentee.print_info()
                submission.print_file_info()
                print()

                answer = prompt_with_options('Choose an option:', options)

            # Score and note
            score = input('Please enter the score: ')
            while not score.isdecimal():
                print('Please enter a number.')
                score = input('Please enter the score: ')
            score = int(score)
            note = ''
            if prompt_with_options('Would you like to add a note?') == 'y':
                print('Please enter the note below.',
                      'Enter a blank line to finish.')
                while True:
                    n = input().strip(' \n\r\t')
                    if len(n) == 0:
                        note = note.rstrip(' \n\r\t')
                        break
                    note += n + '\n'

            submission.assign_result(score, note)

            print()
            print('-' * 12, 'SUMMARY OF SUBMISSION', '-' * 12)
            submission.print_file_info()
            submission.print_evaluation_result()
            print('-' * 47)
            print()

            input('Press ENTER to continue...')
