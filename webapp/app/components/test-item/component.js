import Ember from 'ember';

export default Ember.Component.extend({
    attributeBindings: ['href'],
    tagName: 'a',
    classNames: ['item', 'test', 'clickable'],

    classNameBindings: ['status'],

    test: Ember.computed.oneWay('item'),
    session_model: null,

    status: function() {
        let status = this.get('test.status').toLowerCase();
        if (status === 'failure' || status === 'error') {
            status = 'failed';
        }
        return status;
    }.property('test.status'),

    is_running: Ember.computed.equal('status', 'running'),

    href: function() {
	return `/#/sessions/${this.get('session_model.display_id')}/tests/${this.get('test.display_id')}`;
    }.property('test'),


});
