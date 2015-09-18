import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../mixins/refreshable-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {

    model: function(params) {

        return this.store.find('user', params.email);
    }
});
