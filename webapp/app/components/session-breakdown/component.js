import Ember from 'ember';

var everything = ['num_failed_tests', 'num_error_tests', 'num_skipped_tests', 'num_finished_tests', 'is_running'];

export default Ember.Component.extend({

    session: null,

    tooltip_position: "right",

    total_num_tests: Ember.computed.alias('session.total_num_tests'),
    num_failed_tests: Ember.computed.alias('session.num_failed_tests'),
    num_skipped_tests: Ember.computed.alias('session.num_skipped_tests'),
    num_error_tests: Ember.computed.alias('session.num_error_tests'),
    num_finished_tests: Ember.computed.alias('session.num_finished_tests'),
    is_abandoned: Ember.computed.alias('session.is_abandoned'),

    is_running: function() {
        return this.get('session.is_running') && !this.get('is_abandoned');
    }.property('session'),

    num_successful_tests: function() {
        return this.get('num_finished_tests') - this.get('num_error_tests') - this.get('num_failed_tests') - this.get('num_skipped_tests');
    }.property('session'),

    tooltip_content: function() {
        let returned = this.get('total_num_tests') + " tests collected";

        returned += this._add_counter_summary('Successful', 'num_successful_tests', 'success');
        returned += this._add_counter_summary('Failed', 'num_failed_tests', 'error');
        returned += this._add_counter_summary('Errored', 'num_error_tests', 'error');
        returned += this._add_counter_summary('Skipped', 'num_skipped_tests', 'skip');

        const unrun = this.get('total_num_tests') - this.get('num_finished_tests');

        if (unrun) {
            returned += ' <span class="faint">(' + unrun + ' test' + ((unrun === 1)?'':'s') + ' not run)</span>';
        }

        return returned;

    }.property('session'),

    _add_counter_summary: function(title, attr, classname=null) {
        const value = this.get(attr);

        const tag = (classname===null)?'<strong><span>':('<strong><span class="' + classname + '">');

        if (value) {
            let returned = ', ' + tag + value + '</span></strong> ' + title;
            return returned;
        }

        return '';
    },

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
