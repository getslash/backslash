import Ember from 'ember';

export default Ember.Component.extend({

    tagName: 'span',
    classNames: ['test-name'],

    is_valid_class_name: function() {
        // Deals with a Slash bug that caused incorrect class names to be reported
        // In these cases the class name was wrongfully identified as a portion of the parametrization string when the parameters contained dots
        let name = this.get('info.class_name');
        if (!name) {
            return false;
        }
        if (name.indexOf('(') !== -1) {
            return name.endsWith(')');
        }
        return true;
    }.property('info.class_name'),
});
