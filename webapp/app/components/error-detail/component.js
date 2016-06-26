import Ember from 'ember';

export default Ember.Component.extend({

    error: null,
    loading: false,

    init() {
	let self = this;
	self._super(...arguments);

	let url = self.get('error.traceback_url');
	if (url) {
	    self.set('loading', true);
	    Ember.$.ajax(url, {dataType: 'json'}).then(function(data) {
		self.set('error.traceback', data);
	    }).always(function() {
		self.set('loading', false);
	    });
	}
    },

});
