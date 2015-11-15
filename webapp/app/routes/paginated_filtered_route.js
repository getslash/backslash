import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../mixins/refreshable-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {
    queryParams: {
        page: {
            refreshModel: true
        },
        filter: {
            refreshModel: true,
        }
    },

    resetController: function (controller, isExiting) {
        if (isExiting) {
            controller.set('filter', undefined);
            controller.set('page', 1);
        }
    }



});
