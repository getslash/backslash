import Ember from 'ember';

export default Ember.Component.extend({
    status: null,
    spaced: true,
    classNames: 'status-icon',
    classNameBindings: ['spaced:spaced', 'status_lower'],
    tagName: 'span',

    status_lower: function() {
	let status = this.get('status');
	if (status) {
	    status = status.toLowerCase();
	}
	return status;
    }.property('status'),
});
