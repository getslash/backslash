import Ember from 'ember';

export default Ember.Mixin.create({
    queryParams: ['humanize_times', 'show_successful', 'show_unsuccessful', 'show_abandoned', 'show_skipped'],

    humanize_times: true,
    show_successful: true,
    show_unsuccessful: true,
    show_abandoned: true,
    show_skipped: true,
});
