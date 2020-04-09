class Mentee:
    ID: str
    name: str

    file: str
    submitted: bool
    score: int
    note: str

    def __init__(self, _id: str, name: str):
        self.ID = _id
        self.name = name

    def assign_submission(self, file: str = None):
        if file is None:
            self.submitted = False
            self.score = 0
            return

        self.file = file
        self.submitted = True

    def assign_result(self, score: int, note: str = ''):
        self.score = score
        self.note = note

    def print_file_summary(self):
        print('ID:  ', self.ID)
        print('Name:', self.name)

        if self.submitted:
            print('File:', self.file[self.file.index(']') + 1:])
        else:
            print('No submission.')
        print()

    def print_submission_summary(self):
        print()
        print('-' * 12, 'SUMMARY OF SUBMISSION', '-' * 12)
        self.print_file_summary()

        if self.submitted:
            print('Score:', self.score, sep='\t')

            if self.note:
                print('Note:')
                print(self.note, end='')
        else:
            print('No submission.')

        print('-' * 47)
        print()
