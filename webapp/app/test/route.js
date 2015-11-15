import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {

    title: 'Test Details',

    model: function(params) {
        return this.store.find('test', params.test_id);
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('test', model);

        this.store.find('session', model.get('session_id')).then(
            function(session) {
                model.set('session', session);
            }
        );
    }


});
