import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "row row-fluid session-row",
    session: null,

    click: function() {
        this.sendAction('action', this.get('session'));
    }

});
