import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'a',
    attributeBindings: ['href'],
    classNames: ['item', 'session', 'clickable'],
    classNameBindings: ['item.investigated:investigated', 'item.is_abandoned:abandoned', 'result_type', 'status'],

    session: Ember.computed.oneWay('item'),


    href: function() {
        return '/#/sessions/' + this.get('session.display_id');
    }.property('session.id'),

    status: function() {
        let item = this.get('item');

        if (!item.get('is_abandoned')) {
            if (item.get('num_error_tests') || item.get('num_failed_tests')) {
                return 'failed';
            } else if (item.get('num_skipped_tests')) {
                return 'skipped';
            } else if (item.get('is_running')) {
                return 'running';
            } else if (item.get('num_finished_tests')) {
                return 'success';
            }
        }
    }.property('item.num_skipped_tests', 'item.num_error_tests', 'item.num_failed_tests', 'item.is_running'),

    result_type: Ember.computed.oneWay('item.type'),

    total_num_unsuccessful: function() {
        let item = this.get('item');
        return item.get('num_error_tests') + item.get('num_failed_tests');
    }.property('item.num_error_tests', 'item.num_failed_tests'),

});
