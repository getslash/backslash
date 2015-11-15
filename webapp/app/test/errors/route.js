import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {


    model: function() {
        let test = this.modelFor('test');

        return this.store.query('error', {test_id: test.id});
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('parent_controller', this.controllerFor('test'));
        controller.set('errors', model);
    },

    renderTemplate: function() {
        this.render('errors', {});
  }
});
