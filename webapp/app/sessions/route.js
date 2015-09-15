import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    queryParams: {
        show_archived: {
            refreshModel: true
        }
    },

    model: function(params) {
        return this.store.query('session', {page: params.page, filter: params.filter, show_archived: (params.show_archived)});
    }

});
