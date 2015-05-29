import Ember from 'ember';

/* global moment */

export default Ember.Mixin.create({

    durationMilliseconds: function() {

        return moment(this.get('end_time')).diff(moment(this.get('start_time')));
    }.property('start_time', 'end_time'),

    durationSeconds: function() {

        var d = this.get('durationMilliseconds');
        console.log('d=' + d);
        return d/ 1000;
    }.property('durationMilliseconds'),

    duration: function() {
        return moment.duration(this.get('durationMilliseconds'));
    }.property('durationMilliseconds'),

    humanizedDuration: function() {

        var d = this.get('duration');
        console.log('duration = ' + d);
        return this.get('duration').humanize();
    }.property('duration')
});
