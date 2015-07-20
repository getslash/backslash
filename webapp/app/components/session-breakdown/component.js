import Ember from 'ember';

var everything = ['num_failed_tests', 'num_error_tests', 'num_skipped_tests', 'num_finished_tests', 'is_running'];

export default Ember.Component.extend({

    session: null,

    total_num_tests: Ember.computed.alias('session.total_num_tests'),
    num_failed_tests: Ember.computed.alias('session.num_failed_tests'),
    num_skipped_tests: Ember.computed.alias('session.num_skipped_tests'),
    num_error_tests: Ember.computed.alias('session.num_error_tests'),
    num_finished_tests: Ember.computed.alias('session.num_finished_tests'),
    is_running: Ember.computed.alias('session.is_running'),

    failedPercent: Ember.computed(function() {

        return this._percentOfTotal(parseInt(this.get('num_failed_tests')) + parseInt(this.get('num_error_tests')));
    }).property(...everything),

    has_errors_or_failures: function() {
        return this.get('session.num_errors') || this.get('session.num_failures');
    }.property('session'),

    successPercent: function() {

        return this._percentOfTotal(parseInt(this.get('num_finished_tests')) - parseInt(this.get('num_failed_tests')) - parseInt(this.get('num_error_tests')) - parseInt(this.get('num_skipped_tests')));
    }.property(...everything),

    skipPercent: function() {
        return this._percentOfTotal(this.get('num_skipped_tests'));
    }.property(...everything),

    runningPercent: function() {
        return this._percentOfTotal(1);
    }.property(...everything),

    _percentOfTotal: function(num) {
        let total = this.get('total_num_tests');
        var percentage = 0;
        if (total !== 0) {
            percentage = Math.floor((parseInt(num) / total) * 100);
        }

        return ('width: ' + percentage + '%').htmlSafe();
    }

});
