import Ember from 'ember';

/* global moment */

export default Ember.Component.extend({

    tagName: 'span',

    start_time: null,
    end_time: null,
    is_running: false,

    durationMilliseconds: function() {

        return moment.unix(this.get('end_time')).diff(moment.unix(this.get('start_time')));
    }.property('start_time', 'end_time'),

    durationSeconds: function() {

        var d = this.get('durationMilliseconds');
        return d / 1000;
    }.property('durationMilliseconds'),

    duration: function() {
        return moment.duration(this.get('durationMilliseconds'));
    }.property('durationMilliseconds'),

    humanizedDuration: function() {
        const d = this.get('durationSeconds');
        if (d < 60) {
            return d + 's';
        }
        return this.get('duration').humanize();
    }.property('duration'),

    humanizedEndTime: function() {

        return moment.unix(this.get('end_time')).fromNow();

    }.property('end_time')

});
