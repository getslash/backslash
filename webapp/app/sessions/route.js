import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    queryParams: {
        show_archived: {
            refreshModel: true
        }
    },

    model: function(params) {
        let query_params = {page: params.page, filter: params.filter, show_archived: (params.show_archived)};

        let user_id = this.get_user_id_parameter();

        if (user_id !== undefined) {
            query_params.user_id = user_id;
        }
        return this.store.query('session', query_params);
    },

    get_user_id_parameter: function() {
        return undefined;
    }

});
