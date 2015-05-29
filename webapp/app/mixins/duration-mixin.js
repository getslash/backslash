import Ember from 'ember';

/* global moment */

export default Ember.Mixin.create({

    durationMilliseconds: function() {

        return moment.unix(this.get('end_time')).diff(moment.unix(this.get('start_time')));
    }.property('start_time', 'end_time'),

    startTimeString: function() {
        return this._formatUnixTime(this.get('start_time'));
    }.property('start_time'),

    endTimeString: function() {
        return this._formatUnixTime(this.get('end_time'));
    }.property('end_time'),


    _formatUnixTime: function(m) {
        return moment.unix(m).format('YYYY/MM/DD hh:mm:ss');
    },

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
