import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    needs: 'user',

    model: function() {
        return new Ember.RSVP.hash({
            'user': this.modelFor('user'),
            'tokens': this.api.call('get_user_run_tokens', {user_id: parseInt(this.modelFor('user').id)})
        });
    }
});
