import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'span',

    user_prefs: Ember.inject.service(),

    ago: null,
    time: null,
    unix: null,

    time_value: function() {
	const ago = this.get('ago');
	const time = this.get('time');
	const unix = this.get('unix');


	if (ago !== null) {
	    let value = moment.unix(ago);
	    let now = moment();

	    if (value.isAfter(now)) {
		value = now;
	    }

	    return value.fromNow();
	}

	if (time !== null) {
	    return moment.unix(time).calendar();
	}

	if (unix === null) {
	    return '-';
	}
	return moment.unix(unix);

    }.property('ago', 'time', 'unix'),

    time_string: function() {

	let format = this.get('user_prefs').get_cached('time_format');
	if (!format) {
	    format = 'L LTS';
	}

	let value = this.get('time_value');

	if (value.format !== undefined) {
	    value = value.format(format);
	}
	return value;
    }.property('time_value'),
});
