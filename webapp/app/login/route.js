import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Route.extend(UnauthenticatedRouteMixin, {

    setupController: function(controller) {
        this._super(controller);
        controller.set('loading', false);
        controller.set('torii', this.get('torii'));
    }

});
