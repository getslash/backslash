import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['container-fluid'],
    show_breakdown: true,
    session_model: null,
    user: null,
    metadata: null,

    not_complete: Ember.computed.and('session_model.finished_running', 'session_model.has_tests_left_to_run'),

    slash_version: function() {
	let metadata = this.get('metadata') || {};
	let returned = metadata['slash::version'];
	if (!returned && metadata.slash !== undefined) {
	    returned = metadata.slash.version;
	}
	return returned;
    }.property('metadata'),
});
