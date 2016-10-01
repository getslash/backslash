import Ember from 'ember';

export default Ember.Route.extend({
    model(params) {
	let self = this;
	return self.store.find('test', params.test_id).then(function(test) {
	    return Ember.RSVP.hash({
		test: test,
		session: self.store.find('session', test.get('session_id')),
	    });
	});
    },

    afterModel(model) {
	this.replaceWith('session.test', model.session.get('display_id'), model.test.get('display_id'));
    },

});
