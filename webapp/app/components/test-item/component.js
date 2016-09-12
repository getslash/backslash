import Ember from 'ember';

export default Ember.Component.extend({
    attributeBindings: ['href'],
    tagName: 'a',
    classNames: ['item', 'test', 'clickable'],

    classNameBindings: ['status', 'has_any_error:unsuccessful'],

    test: Ember.computed.oneWay('item'),
    session_model: null,

    has_any_error: function() {
	let item = this.get('item');

	return item.get('num_errors') || item.get('num_failures');
    }.property('item.num_errors', 'item.num_failures'),


    status: function() {
        let status = this.get('test.status').toLowerCase();
        if (status === 'failure' || status === 'error') {
            status = 'failed';
        }
        return status;
    }.property('test.status'),

    is_running: function() {
	let session = this.get('session_model');
	if (session && session.get('is_abandoned')) {
	    return false;
	}
	return this.get('status') === 'running';
    }.property('session_model', 'status'),

    href: function() {
	let returned = `/#/sessions/${this.get('test.session_display_id')}/tests/${this.get('test.display_id')}`;
	if (this.get('has_any_error')) {
	    returned += '/errors';
	}
	return returned;
    }.property('test'),


});
