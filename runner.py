import os.path
import subprocess
import sys
from typing import Dict
from models import Mentee
from environment import *


def make_input_file():
    with open(INPUT_FILE, 'w', encoding='utf-8') as input_file:
        create_input = prompt_with_options(
            "Would you like to create a common"
            "input file for all submissions?",
            ['yes', 'no']
        )
        if create_input == 'yes':
            print('Please enter the input data below.',
                  'Enter a blank line to finish.')
            data = ''
            while True:
                inp = input().strip(' \n\r\t')
                if len(inp) == 0:
                    input_file.write(data)
                    break
                data += inp + '\n'
        else:
            input_file.write('')
        input_file.close()

    return create_input == 'yes'


def prompt_with_options(prompt: str, options: [str] = None) -> str:
    if options is None:
        options = ['y', 'n']
    while True:
        char = input('{} ({}) '.format(prompt, '/'.join(options))) \
            .strip(' \n\r\t')
        if char in options:
            return char
        choices = ', '.join(options[:-1]) + ' and {}'.format(options[-1])
        print("Please select between {}.".format(choices))


def run_c_file(file: str, feed_input: bool = False):
    if not file.endswith('.c'):
        print('File {} is not a .c file!'.format(file))
        return

    if not os.path.isdir(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)

    with open(INPUT_FILE, encoding='utf-8') as input_file:
        file_name = file.rstrip('.c').split('/')[-1]
        output_file = '{}/{}.out'.format(OUTPUT_DIRECTORY, file_name)
        if sys.platform == 'win32':
            pass
        else:
            try:
                subprocess.run(['gcc', '-o', output_file, file])
                if feed_input:
                    subprocess.run(output_file, stdin=input_file)
                else:
                    subprocess.run(output_file)
            except FileNotFoundError:
                print('Compile error has occurred')

        input_file.close()


def run_py_file(file: str, feed_input: bool = False):
    if not file.endswith('.py'):
        print('File {} is not a .py file!'.format(file))
        return

    with open(INPUT_FILE, encoding='utf-8') as input_file:
        if sys.platform == 'win32':
            if feed_input:
                subprocess.run(['python', file], stdin=input_file)
            else:
                subprocess.run(['python', file])
        else:
            if feed_input:
                subprocess.run(['python3', file], stdin=input_file)
            else:
                subprocess.run(['python3', file])
        input_file.close()


def runner(mentees: Dict[str, Mentee]):
    feed_input_file = make_input_file()

    with_submission = list(filter(lambda m: m.submitted, mentees.values()))
    for mentee in with_submission:
        for submission in mentee.submissions:
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
                        run_c_file(submission.file, feed_input_file)
                    elif file_extension == '.py':
                        run_py_file(submission.file, feed_input_file)
                    else:
                        print('Extension .{} is not yet supported!'.format(
                            file_extension))
                    print()
                    print('-' * 12, 'END OF OUTPUT', '-' * 12)
                    print()
                if answer == 'code':
                    print()
                    print('-' * 12, 'BEGINNING OF CODE', '-' * 12)
                    submission.print_file_content()
                    print()
                    print('-' * 12, 'END OF CODE', '-' * 12)
                    print()
                if answer == 'evaluate':
                    break

                mentee.print_info()
                submission.print_file_info()
                print()

                options = ['run', 'code', 'evaluate']
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
