import Ember from 'ember';

import {momentRange} from '../../helpers/moment-range';

/* global moment */

export default Ember.Component.extend({

    tagName: 'span',
    start_time: null,
    end_time: null,

    corrected_end_time: function(){
    	return this.get('end_time')?this.get('end_time'):moment().unix();
    }.property('end_time'),

    humanized_range: function() {
        return momentRange([], {start_time: this.get('start_time'),
                                end_time: this.get('corrected_end_time')});
    }.property('start_time', 'corrected_end_time'),

    duration_milliseconds: function() {

        return moment.unix(this.get('corrected_end_time')).diff(moment.unix(this.get('start_time')));
    }.property('start_time', 'corrected_end_time'),

    duration_seconds: function() {
        var d = this.get('duration_milliseconds');

        if (!d) {
            return null;
        }

        return d / 1000;
    }.property('duration_milliseconds'),

    duration: function() {
        return moment.duration(this.get('duration_milliseconds'));
    }.property('duration_milliseconds'),

    humanized_duration: function() {
        const d = this.get('duration_seconds');

        if (!d) {
            return '-';
        }

        if (d < 60) {
            return d + ' seconds';
        }
        let returned = this.get('duration').humanize();
	if (!this.get('end_time')) {
	    returned += ' (not finished)';
	}
	return returned;
    }.property('duration','duration_seconds'),

});
