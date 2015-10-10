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

     setupController: function(controller, model) {
         this._super(controller, model);
         controller.set('pages_total', model.get('meta.pages_total'));
         controller.set('filter_config', model.get('meta.filter_config'));
    },

    resetController: function (controller, isExiting) {
        if (isExiting) {
            controller.set('filter', undefined);
            controller.set('page', 1);
        }
    }



});
