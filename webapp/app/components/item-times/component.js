import Ember from 'ember';

/* global moment */

export default Ember.Component.extend({

    classNames: ['times'],

    start: null,
    end: null,
    humanize: true,

    raw_times_text: function() {
        let start = this.get('start');
        let end = this.get('end');

        let returned = this._format(start) + ' - ';
        if (end) {
            returned += this._format(end);
        } else {
            returned += '...';
        }

        return returned;

    }.property('start', 'end'),

    humanized_text: function() {
        let start = this.get('start');
        let end = this.get('end');

        if (!end) {
            return 'Started ' + this._humanize(start);
        }
        return 'Finished ' + this._humanize(end);

    }.property('start', 'end'),

    _humanize(t) {
        let now = moment();
        t = moment.unix(t);

        if (t.isAfter(now)) {
            t = now;
        }
        return t.fromNow();
    },

    _format(t) {
        return moment.unix(t).format('L LTS');
    },
});
