import Ember from 'ember';

export default Ember.Service.extend({

  set_by_session(session) {
    this.reset();
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
    this.reset();
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
    this._set('/assets/img/icons/backslash-success-favicon.png');
  },

  set_failure() {
    this._set('/assets/img/icons/backslash-failure-favicon.png');
  },

  reset() {
    this._set('/assets/img/icons/backslash-favicon.png');
  },

  _set(url) {

    Ember.$('#favicon').attr('href', url);
  },
});
