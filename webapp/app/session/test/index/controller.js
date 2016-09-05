import Ember from 'ember';

export default Ember.Controller.extend({
    additional_metadata: function() {
	return {
	};
    }.property('test'),

    scm_details: function() {
	let self = this;
	let test = self.get('test_model');

	if (!test.get('scm')) {
	    return {};
	}

	return Ember.Object.create({
	    'Revision': test.get('scm_revision'),
	    'File Hash': test.get('file_hash')
	});

    }.property('test'),
});
