import Ember from 'ember';

export default Ember.Component.extend({
    tagName: 'ul',

    classNames: "nav navbar-nav navbar-right",
    dropdown_id: function() {
        return `dropdown-${this.elementId}`;
    }.property(),


});
