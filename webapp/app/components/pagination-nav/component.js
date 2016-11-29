import Ember from 'ember';

export default Ember.Component.extend({

    page: 1,
    has_next: false,

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
