import sys


class Mentee:
    def __init__(self, _id: str, name: str):
        self.ID = _id
        self.name = name

        self.submissions = []
        self.submitted = False

    def assign_submission(self, file: str = None):
        if file is None:
            return

        submission = Submission(file, self)
        self.submissions.append(submission)
        self.submitted = True

    def print_info(self):
        print('ID:\t', self.ID)
        print('Name:\t', self.name)

    def print_submissions_summary(self):
        self.print_info()
        if self.submitted:
            for submission in self.submissions:
                submission.print_file_info()
                submission.print_evaluation_result()
        else:
            print('No submission.')


class Submission:
    @property
    def file_extension(self):
        return '.'+self.file.split('.')[-1]

    @property
    def file_name(self):
        if sys.platform == 'win32':
            return self.file.split('\\')[-1]
        else:
            return self.file.split('/')[-1]

    def __init__(self, file: str, mentee: Mentee):
        self.file = file
        self.mentee_id = mentee.ID
        self.mentee_name = mentee.name
        self.score = 0
        self.note = ''

    def assign_result(self, score: int, note: str = ''):
        self.score = score
        self.note = note

    def print_file_content(self):
        empty_line = False
        with open(self.file, encoding='utf-8') as opened_file:
            for line in opened_file.readlines():
                empty_line = len(line.rstrip(' \n\r\t')) == 0
                print(line.rstrip(' \n\r\t'))
            opened_file.close()
            if empty_line:
                print()

    def print_file_info(self):
        print('File:', self.file_name)

    def print_evaluation_result(self):
        print('Score:', self.score, sep='\t')

        if self.note != '':
            print('Note:')
            print(self.note)
