import Ember from 'ember';

export default Ember.Component.extend({

    page: 1,
    has_next: false,

    has_prev: Ember.computed.gt('page', 1),

    actions: {

	first_page() {
	    this.set('page', 1);
	},

	next_page() {
	    this.incrementProperty('page');
	},

	prev_page() {
	    this.decrementProperty('page');
	},

    },
});
