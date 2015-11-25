import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "counter",
    classNameBindings: ['class_name', 'visibility_class_name', 'has_caption:varwidth'],

    tooltip: function() {
        return this.get('counter') + ' ' + this.get('artifact_name') + 's';
    }.property('artifact_name', 'counter'),

    fixed_width: false,

    warnings: null,
    errors: null,
    caption: null,

    has_caption: Ember.computed.notEmpty('caption'),

    icon: function() {
        if (this.get('warnings')) {
            return 'warning';
        }
        return 'times-circle';
    }.property('warnings', 'errors'),


    visibility_class_name: function() {
        if (!this.get('counter')) {
            if (this.get('fixed_width')) {
                return 'noshow';
            }
            return 'hidden';
        }
    }.property('counter', 'fixed_width'),

    counter: Ember.computed.or('warnings', 'errors'),

    artifact_name: function() {
        if (this.get('warnings')) {
            return 'warning';
        } else if (this.get('errors')) {
            return 'error';
        }
    }.property('warnings', 'errors'),

    class_name: Ember.computed.oneWay('artifact_name'),

});
