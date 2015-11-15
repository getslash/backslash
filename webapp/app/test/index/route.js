import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {

    model: function() {
        return this.modelFor('test');
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('parent_controller', this.controllerFor('test'));
    }
});
