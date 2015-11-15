import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    model: function(params) {

        return this.store.find('error', params.error_id);
    },


    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('error', model);
        controller.set('test', this.controllerFor('test').get('test'));
        controller.set('session', this.controllerFor('test').get('test.session'));

    },

    renderTemplate: function() {
        this.render('single_error');
    }

});
