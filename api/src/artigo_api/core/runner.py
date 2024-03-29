class PytestTestRunner:
    def __init__(self, verbosity=1, failfast=False, keepdb=False, **kwargs):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument(
            '--keepdb', action='store_true',
            help='Preserve test DB between runs.',
        )

    def run_tests(self, test_labels):
        import pytest

        argv = []

        if self.verbosity == 0:
            argv.append('--quiet')
        elif self.verbosity == 2:
            argv.append('--verbose')
        elif self.verbosity == 3:
            argv.append('-vv')

        if self.failfast:
            argv.append('--exitfirst')

        if self.keepdb:
            argv.append('--reuse-db')

        argv.extend(test_labels)

        return pytest.main(argv)
