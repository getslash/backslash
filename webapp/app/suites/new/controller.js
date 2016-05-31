import Ember from 'ember';

export default Ember.Controller.extend({

    reset() {
	this.set('suite_name', '');
	this.set('error', null);
    },

    suite_name_valid: Ember.computed.notEmpty('suite_name'),

    is_valid: Ember.computed.alias('suite_name_valid'),


    actions: {
	create() {
	    let self = this;
	    return self.api.call('create_suite', {
		name: self.get('suite_name'),
	    }).error(function(e) {
		self.set('error', e.responseJSON.message);
	    }).success(function() {
		self.router.transitionTo('suites.index');

	    });
	}
    },
});
