import Ember from 'ember';

import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend({

    model: function(params) {
        let test = this.modelFor('test');

        return Ember.RSVP.hash({
            test: test,
            session: this.store.find('session', test.get('session_id')),
            errors: this.store.query('error', {test_id: test.id, page: params.page})
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
        controller.setProperties({
            single_error_route_name: 'test.single_error',
            parent_id: model.test.id
        });
    },

    renderTemplate: function() {
        this.render('errors', {});
    },

    afterModel(model) {
        if (model.errors.get('meta.total') === 1) {
          this.transitionTo('test.single_error', 1);
        }
    }
});
