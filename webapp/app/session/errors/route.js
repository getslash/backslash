import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {


    model: function() {
        let session = this.modelFor('session');

        return this.store.query('error', {session_id: session.id});
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('session', this.modelFor('session'));
        controller.set('errors', model);
    },

    renderTemplate: function() {
        this.render('errors');
    }
});
