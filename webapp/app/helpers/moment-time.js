import Ember from 'ember';

/* global moment */

export function momentTime(params, opts) {

    if (opts.ago !== undefined) {

        return moment.unix(opts.ago).fromNow();
    }

    if (opts.unix === null) {
        return '-';
    }
    return moment.unix(opts.unix).format('YYYY/MM/DD hh:mm:ss');
}

export default Ember.Helper.helper(momentTime);
