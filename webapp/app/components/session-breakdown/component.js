import Ember from 'ember';

var everything = ['num_failed_tests', 'num_error_tests', 'num_skipped_tests', 'num_finished_tests', 'is_running'];

export default Ember.Component.extend({

    session: null,

    num_failed_tests: Ember.computed.alias('session.num_failed_tests'),
    num_skipped_tests: Ember.computed.alias('session.num_skipped_tests'),
    num_error_tests: Ember.computed.alias('session.num_error_tests'),
    num_finished_tests: Ember.computed.alias('session.num_finished_tests'),
    is_running: Ember.computed.alias('session.is_running'),

    failedPercent: Ember.computed(function() {

        return this._percentOfTotal(parseInt(this.get('num_failed_tests')) + parseInt(this.get('num_error_tests')));
    }).property(...everything),

    successPercent: function() {

        return this._percentOfTotal(parseInt(this.get('num_finished_tests')) - parseInt(this.get('num_failed_tests')) - parseInt(this.get('num_error_tests')) - parseInt(this.get('num_skipped_tests')));
    }.property(...everything),

    skipPercent: function() {
        return this._percentOfTotal(this.get('num_skipped_tests'));
    }.property(...everything),


    _percentOfTotal: function(num) {

        var finished = parseInt(this.get('num_finished_tests'));
        if (finished === 0) {
            return "width: 0%".htmlSafe();
        }
        var percentage = Math.floor(parseInt(num) / finished * (this.get('is_running')?70:100));


        return ('width: ' + percentage + '%').htmlSafe();
    }

});
