import filter
import manager
import runner
from environment import RESULT_CSV


def main():
    mentees = manager.create_mentees()

    filter.filter_files(mentees)
    filter.print_filtering_result(mentees)
    input('Press ENTER to continue...')

    runner.runner(mentees)
    print('Evaluation finished!')

    manager.create_result_csv(mentees)
    print('{} has been created.'.format(RESULT_CSV))

    if input('Clean up submission and output directories? [Y] ') == 'Y':
        filter.cleanup_files()


if __name__ == "__main__":
    main()
