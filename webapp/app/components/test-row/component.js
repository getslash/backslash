import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "row row-fluid test-row",

    click: function() {
        this.sendAction('gotoTest', this.test);
    }
});
