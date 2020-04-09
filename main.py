import fileFilter
import menteesManager
import submissionRunner
from environment import RESULT_CSV


def main():
    mentees = menteesManager.create_mentees()

    fileFilter.filter_files(mentees)
    fileFilter.print_submission_result(mentees)
    input('Press ENTER to continue...')

    submissionRunner.runner(mentees)
    print('Evaluation finished!')

    menteesManager.create_result_csv(mentees)
    print('{} has been created.'.format(RESULT_CSV))


if __name__ == "__main__":
    main()
