import Ember from 'ember';

/* global moment */

export function momentRange(params, opts) {

    if (opts.start_time === undefined) {
    	return '-';
    }

    if (opts.end_time === undefined){
        return moment.unix(opts.ago).calendar();
    }

    let range = moment.unix(opts.start_time).twix(moment.unix(opts.end_time));

    if (opts.expanded) {
         return range.simpleFormat('YYYY/MM/DD hh:mm:ss');
    }
    return range.format();
}

export default Ember.Helper.helper(momentRange);
