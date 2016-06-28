import Ember from 'ember';

export default Ember.Component.extend({

    saving: false,

    actions: {

	choose: function(option) {
	    this.sendAction("action", option);
	},
    },

});
