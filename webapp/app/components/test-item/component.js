import Ember from 'ember';

export default Ember.Component.extend({
    display: Ember.inject.service(),
    attributeBindings: ['href'],
    tagName: 'a',
    classNames: ['item', 'test', 'clickable'],

    classNameBindings: ['test.computed_status', 'test.has_any_error:unsuccessful'],

    test: Ember.computed.oneWay('item'),
    session_model: null,

    is_running: Ember.computed.equal('test.computed_status', 'running'),

    href: function() {
	let returned = `/#/sessions/${this.get('test.session_display_id')}/tests/${this.get('test.display_id')}`;
	if (this.get('test.has_any_error')) {
	    returned += '/errors';
	}
	return returned;
    }.property('test'),


});
