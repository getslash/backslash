import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "row row-fluid test-row",

    icon_classes: function() {
        const test = this.get('test');

        if (test.get('is_running')) {
            return 'fa-spin fa-cog running';
        } else if (test.get('is_skipped')) {
            return 'fa-arrow-circle-o-right skipped';
        } else if (test.get('is_success')) {
            return 'fa-check-circle success';
        } else {
            return 'fa-times failure';
        }
    }.property('test'),

    click: function() {
        this.sendAction('action', this.get('test'));
    }
});
