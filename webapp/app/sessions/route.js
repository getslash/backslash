import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import PollingRoute from '../mixins/polling-route';
import ScrollToTopMixin from '../mixins/scroll-top';
import StatusFilterableRoute from '../mixins/status-filterable/route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, PollingRoute, ScrollToTopMixin, StatusFilterableRoute, {

    titleToken: 'Sessions',

    model(params) {
        let query_params = {page: params.page, filter: params.filter, page_size: params.page_size};
        this.transfer_filter_params(params, query_params);

        let user_id = this.get_user_id_parameter();

        if (user_id !== undefined) {
            query_params.user_id = user_id;
        }
        return this.store.query('session', query_params);
    },

    setupController(controller, model) {
        controller.set('sessions', model);
    },

    get_user_id_parameter: function() {
        return undefined;
    },

});
