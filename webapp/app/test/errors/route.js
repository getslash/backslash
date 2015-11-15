import Ember from 'ember';

import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {


    model: function() {
        let test = this.modelFor('test');

        return Ember.RSVP.hash({
            test: test,
            session: this.store.find('session', test.get('session_id')),
            errors: this.store.query('error', {test_id: test.id})
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
        controller.setProperties({
            single_error_route_name: 'test.single_error',
            parent_id: model.session.id
        });
    },

    renderTemplate: function() {
        this.render('errors', {});
    }
});
