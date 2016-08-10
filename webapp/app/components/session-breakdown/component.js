import Ember from 'ember';

export default Ember.Component.extend({

    session: null,

    data: function() {
	const returned = {
	    columns: this._get_columns(),
	    type: 'donut',
	    colors: {
		failed: '#d9534f',
		errored: 'red',
		skipped: '#f0ad4e',
		successful: '#5cb85c',
	    }
	};
	console.table(returned.columns);
	return returned;
    }.property('session'),

    _get_columns() {
	let s = this.get('session');

	let all = [
		['failed', s.get('num_failed_tests')],
		['errored', s.get('num_error_tests')],
		['skipped', s.get('num_skipped_tests')],
		['successful', this.get('num_successful_tests')],
	    ];
	let returned = [];
	for (let item of all) {
	    if (item[1]) {
		returned.push(item);
	    }
	}
	return returned;
    },

    num_successful_tests: function() {
        return this.get('session.num_finished_tests') - this.get('session.num_error_tests') - this.get('session.num_failed_tests') - this.get('session.num_skipped_tests');
    }.property('session'),

    donut: {
	title: 'Session breakdown',
    },

    tooltip: {
	format: {
	    value: function(value) {
		return value;
	    },
	},
    },

});
