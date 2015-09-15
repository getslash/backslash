import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Controller.extend(UnauthenticatedRouteMixin, {
    authenticator: 'authenticator:torii'
});
