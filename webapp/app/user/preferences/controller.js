import Ember from 'ember';

/* global moment */

export default Ember.Controller.extend({

    user_prefs: Ember.inject.service(),
    saving: false,

    time_format: Ember.computed.oneWay('model.time_format'),

    time_formats: [
	'DD/MM/YYYY HH:mm:ss',
	'DD/MM/YYYY HH:mm',
	'YYYY-MM-DD HH:mm:ss',
    ],

    display_time_formats: function() {
	let returned = [];
	let formats = this.get('time_formats');

	let now = moment();

	for (let fmt of formats) {
	    returned.push(now.format(fmt));
	}

	return returned;
    }.property('time_formats'),

    actions: {
	choose_option: function(option_name, value) {
	    let self = this;

	    self.set('saving', true);
	    self.get('user_prefs').set_pref(option_name, value).then(function(new_value) {
		self.set(option_name, new_value);
	    }).always(function() {
		self.set('saving', false);
	    });
	},
    },
});
