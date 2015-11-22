import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "inline-block",

    test: null,

    display_tooltip: Ember.computed.or('test.first_error', 'test.skip_reason'),

    status: function() {
        return this.get('test.status').toLowerCase();
    }.property('test.status'),

    tooltip_html: function() {
        let text = null;
        const skip_reason = this.get('test.skip_reason');
        const first_error = this.get('test.first_error');
        console.log('s=', skip_reason, 'f=', first_error);

        if (skip_reason) {
            text = skip_reason;
        } else if (first_error) {
            text = first_error.exception_type + ': ' + first_error.message;
        } else {
            return null;
        }

        if (text.length > 50) {
            text = text.substr(0, 50) + '...';
        }

        let returned = '<span class="error-preview"><i class="fa fa-exclamation"></i> ' + text + '</span>';
        console.log('returning', returned);
        return returned;
    }.property('test.first_error', 'test.skip_reason'),

    tooltip_class: function() {
        if (this.get('test.skip_reason')) {
            return 'tooltipster-skip-reason';
        }
        return "tooltipster-error-preview";
    }.property('test')

});
