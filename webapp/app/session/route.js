import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ScrollToTopMixin from '../mixins/scroll-top';

export default Ember.Route.extend(AuthenticatedRouteMixin, ScrollToTopMixin, {


    model: function(params) {
        return this.store.find('session', params.id);
    }

});
