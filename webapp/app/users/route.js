import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    titleToken: 'Users',

    queryParams: {
        sort: {
            refreshModel: true,
        }
    },

    model: function(params) {
        return this.store.query('user', {page: params.page, sort: params.sort});
    }
});
