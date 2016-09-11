import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'a',
    attributeBindings: ['href'],
    classNames: ['item', 'session', 'clickable'],
    classNameBindings: ['item.investigated:investigated', 'is_abandoned:abandoned', 'result_type', 'status', 'in_pdb:pdb', 'interrupted:interrupted', 'has_any_error:unsuccessful'],

    session: Ember.computed.alias('item'),


    href: function() {
        return '/#/sessions/' + this.get('session.display_id');
    }.property('session.id'),

    in_pdb: Ember.computed.oneWay('session.in_pdb'),

    interrupted: Ember.computed.and('item.finished_running', 'item.has_tests_left_to_run'),

    has_any_error: function() {
	let item = this.get('item');

	return item.get('num_error_tests') || item.get('num_failed_tests') || item.get('num_errors');
    }.property('item.num_failed_tests', 'item.num_error_tests', 'item.num_errors'),


    status: function() {
        let item = this.get('item');
	let status = item.get('status');

	if (status) {
	    status = status.toLowerCase();
	}

        if (!item.get('is_abandoned')) {
            if (!item.get('is_running') && this.get('has_any_error')) {
                return 'failed';
            } else if (['error', 'failure'].indexOf(status) !== -1) {
                return 'failed';
	    } else if (item.get('is_interrupted')) {
		return 'interrupted';
            } else if (item.get('is_running')) {
                return 'running';
            } else if (item.get('num_skipped_tests')) {
                return 'skipped';
            } else if (item.get('num_finished_tests')) {
                return 'success';
            } else {
                return 'finished';
            }
        }
    }.property('item.num_skipped_tests', 'has_any_error', 'item.is_running', 'item.status'),

    result_type: Ember.computed.oneWay('item.type'),

    abandoned_reason: function() {
        if (this.get('session.is_abandoned')) {
            return 'Never completed';
        } else if (!this.get('session.num_finished_tests') && this.get('session.end_time')) {
            return 'Ended; No finished tests';
        }
    }.property('session.is_abandoned', 'session.num_finished_tests'),

    is_abandoned: Ember.computed.notEmpty('abandoned_reason'),

    total_num_unsuccessful: function() {
        let item = this.get('item');
        return item.get('num_error_tests') + item.get('num_failed_tests');
    }.property('item.num_error_tests', 'item.num_failed_tests'),

});
