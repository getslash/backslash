import Ember from 'ember';

/* global moment */

export function momentTime(params, opts) {

    let format = opts.format;
    if (format === undefined) {
	format = 'L LTS';
    }

    if (opts.ago !== undefined) {
        let value = moment.unix(opts.ago);
        let now = moment();

        if (value.isAfter(now)) {
            value = now;
        }

        return value.fromNow();
    }

    if (opts.time !== undefined) {
    	return moment.unix(opts.time).calendar();
    }

    if (opts.unix === null) {
        return '-';
    }
    return moment.unix(opts.unix).format(format);
}

export default Ember.Helper.helper(momentTime);
