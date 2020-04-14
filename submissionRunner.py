import subprocess
import sys
from typing import Dict
from Mentee import Mentee


def prompt_with_options(prompt: str, options: [str] = None) -> str:
    if options is None:
        options = ['y', 'n']
    while True:
        char = input('{} ({}) '.format(prompt, '/'.join(options)))
        if char in options:
            return char
        choices = ','.join(options[:-1]) + ' and {}'.format(options[-1])
        print("Please select between {}.".format(choices))


def runner(mentees: Dict[str, Mentee]):
    with_submission = list(filter(lambda m: m.submitted, mentees.values()))

    for mentee in with_submission:
        options = ['run', 'code', 'evaluate']
        answer = 'run'
        while True:
            if answer == 'run':
                print()
                print('-' * 12, 'BEGINNING OF OUTPUT', '-' * 12)
                if sys.platform == 'win32':
                    subprocess.call(['python', mentee.file])
                else:
                    subprocess.call(['python3', mentee.file])
                print('-' * 12, 'END OF OUTPUT', '-' * 12)
                print()
            if answer == 'code':
                file = open(mentee.file, encoding='utf-8')
                print()
                print('-' * 12, 'BEGINNING OF CODE', '-' * 12)
                for line in file.readlines():
                    print(line.rstrip(' \n\r\t'))
                print('-' * 12, 'END OF CODE', '-' * 12)
                print()
                file.close()
            if answer == 'evaluate':
                break

            mentee.print_file_summary()
            answer = prompt_with_options('Choose an option:', options)

        # Score and note
        score = input('Please enter the score: ')
        while not score.isdecimal():
            print('Please enter a number.')
            score = input('Please enter the score: ')
        score = int(score)
        note = ''
        if prompt_with_options('Would you like to add a note?') == 'y':
            print('Please enter the note below. Enter a blank line to finish.')
            while True:
                n = input().strip(' \n\r\t')
                if len(n) == 0:
                    break
                note += n + '\n'

        mentee.assign_result(score, note)
        mentee.print_submission_summary()

        input('Press ENTER to continue...')
