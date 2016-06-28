import Ember from 'ember';

export default Ember.Service.extend({
    call: function(name, params={}) {
	return Ember.$.ajax({
	    type: 'POST',
	    url: '/api/' + name,
	    contentType: 'application/json',
	    data: JSON.stringify(params)
	});
    },

});
