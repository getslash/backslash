import Ember from 'ember';

export default Ember.Service.extend({

  set_by_session(session) {
    let status = session.get('computed_status');

    if (status) {
      status = status.toLowerCase();
      if (status === 'success' || status == 'skipped') {
        this.set_success();
      } else if (!session.is_ok()) {
        this.set_failure();
      }
    }
  },

  set_by_test(test) {
    let status = test.get('computed_status');

    if (status) {
      status = status.toLowerCase();

      if (status === 'success' || test.get('is_skipped')) {
        this.set_success();
      } else if (!test.get('is_running') || test.get('has_any_error')) {
        this.set_failure();
      }
    }
  },

  set_success() {
    this._set('backslash-success-favicon.png');
  },

  set_failure() {
    this._set('backslash-failure-favicon.png');
  },

  reset() {
    this._set('backslash-favicon.png');
  },

  _set(name) {

    Ember.$('#favicon').attr('href', `/assets/img/icons/${name}`);
  },
});
