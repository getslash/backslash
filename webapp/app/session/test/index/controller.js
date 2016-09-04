import Ember from 'ember';

export default Ember.Controller.extend({
    additional_metadata: function() {
	return {
	};
    }.property('test'),
});
