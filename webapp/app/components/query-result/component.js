import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['query-result', 'clickable'],
    classNameBindings: ['result.investigated:investigated', 'result.is_abandoned:abandoned', 'result_type', 'quick_status'],
    result: null,

    quick_status: function() {
        let result = this.get('result');

        if (result.get('num_error_tests') || result.get('num_failed_tests')) {
            return 'failed';
        } else if (result.get('num_skipped_tests')) {
            return 'skipped';
        } else if (result.get('is_running')) {
            return 'running';
        } else {
            return 'success';
        }
    }.property('result.num_skipped_tests', 'result.num_error_tests', 'result.num_failed_tests', 'result.is_running'),

    result_type: Ember.computed.oneWay('result.type'),

    typename: Ember.computed.oneWay('result.type'),

    click: function() {
        this.sendAction('route_to', this.get('typename'), this.get('result.display_id'));
    },


});
