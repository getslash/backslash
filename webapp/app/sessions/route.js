import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import PollingRoute from '../mixins/polling-route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, PollingRoute, {

    titleToken: 'Sessions',

    queryParams: {
        humanize_times: {
            refreshModel: false,
        },
        page: {
            refreshModel: true
        },
        filter: {
            refreshModel: true,
        }
    },


    model(params) {
        let query_params = {page: params.page, filter: params.filter};

        let user_id = this.get_user_id_parameter();

        if (user_id !== undefined) {
            query_params.user_id = user_id;
        }
        query_params.page_size = 50;
        return this.store.query('session', query_params);
    },

    setupController(controller, model) {
        controller.set('sessions', model);
    },

    get_user_id_parameter: function() {
        return undefined;
    },

});
