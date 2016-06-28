import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
    api: Ember.inject.service(),

    model() {
        return this.get('api').call('get_admin_stats').then(function(result) {
            return result.result;
        });
    }
});
