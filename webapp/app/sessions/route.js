import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import PollingRoute from '../mixins/polling-route';
import ScrollToTopMixin from '../mixins/scroll-top';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, PollingRoute, ScrollToTopMixin, {

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
        },
        show_successful: {
            refreshModel: true,
        },
        show_unsuccessful: {
            refreshModel: true,
        },
        show_abandoned: {
            refreshModel: true,
        },
        show_skipped: {
            refreshModel: true,
        },
    },


    model(params) {
        let query_params = {page: params.page, filter: params.filter, page_size: params.page_size};
        for (let key in params) {
            if (key.startsWith('show_')) {
                query_params[key] = params[key];
            }
        }

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
