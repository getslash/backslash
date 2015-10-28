import Ember from 'ember';

export default Ember.Component.extend({

    classNames: "row row-fluid session-row",
    classNameBindings: ['session.investigated:investigated', 'session.is_abandoned:abandoned'],

    session: null,

    click: function() {
        this.sendAction('action', this.get('session'));
    }

});
