def test_report_in_pdb(started_session):
    assert not started_session.in_pdb
    started_session.report_in_pdb()
    assert started_session.refresh().in_pdb
    started_session.report_not_in_pdb()
    assert not started_session.refresh().in_pdb


def test_report_in_pdb_end_session(started_session):
    assert not started_session.in_pdb
    started_session.report_in_pdb()
    assert started_session.refresh().in_pdb
    started_session.report_end()
    assert not started_session.refresh().in_pdb
