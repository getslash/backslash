import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import PaginatedFilteredRoute from '../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    title: 'Test Information',

    model(params) {
        let test_info_id = params.id;

        return Ember.RSVP.hash({
            tests: this.store.query('test', {
                info_id: test_info_id,
                filter: params.filter,
                page: params.page,
            }),
            test_info: this.store.find('test-info', test_info_id),
        });
    },

    setupController(controller, model) {
        console.log('setting up', controller, 'with', model);
        controller.setProperties(model);
    },

});
