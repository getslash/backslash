import Ember from 'ember';

export default Ember.Component.extend({

    session: null,

    classNames: ['session-breakdown'],

    data: function() {
	const returned = {
	    columns: this._get_columns(),
	    type: 'donut',
	    colors: {
		failed: '#d9534f',
		errored: 'red',
		skipped: '#f0ad4e',
		successful: '#5cb85c',
		'not run': 'silver',
	    },
	    labels: true,
	};
	return returned;
    }.property('session'),

    _get_columns() {
	let s = this.get('session');

	let all = [
		['failed', s.get('num_failed_tests')],
		['errored', s.get('num_error_tests')],
		['skipped', s.get('num_skipped_tests')],
		['successful', this.get('num_successful_tests')],
	        ['not run', this.get('num_not_run_tests')],
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

    size: {
	width: 400,
    },

    num_not_run_tests: function() {
	let total = this.get('session.total_num_tests');
	if (!total) {
	    return null;
	}
	return total - this.get('session.num_finished_tests');
    }.property('session'),

    donut: function() {
	let session = this.get('session');
	return {
	    width: 8,
	    label: {
		show: false,
	    },
	    title: `${session.get('total_num_tests')} tests`,
	};
    }.property('session'),

    tooltip: {
	format: {
	    value: function(value) {
		return value;
	    },
	},
    },

});
