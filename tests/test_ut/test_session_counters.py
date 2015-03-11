def test_session_counts_initial(started_session):
    started_session.refresh()
    assert started_session.num_failed_tests == 0
    assert started_session.num_error_tests == 0
    assert started_session.num_skipped_tests == 0
    assert started_session.num_finished_tests == 0


def test_session_counts(started_session):

    counts = {
        'num_failed_tests': 3,
        'num_error_tests': 2,
        'num_skipped_tests': 4,
        'num_finished_tests': 16,
    }

    remaining = counts.copy()
    while remaining['num_finished_tests']:
        remaining['num_finished_tests'] -= 1

        test = started_session.report_test_start(name='test')

        if remaining['num_failed_tests']:
            test.add_failure()
            remaining['num_failed_tests'] -= 1
        elif remaining['num_error_tests']:
            test.add_error()
            remaining['num_error_tests'] -= 1
        elif remaining['num_skipped_tests']:
            test.mark_skipped()
            remaining['num_skipped_tests'] -= 1

        test.report_end()

    started_session.report_end()

    started_session.refresh()

    for key, value in counts.items():
        assert getattr(started_session, key) == value
