import Ember from 'ember';

export default Ember.Route.extend({

    beforeModel: function() {
        this.transitionTo('user', this.get('session.content.user_info.user_id'));
    }
});
