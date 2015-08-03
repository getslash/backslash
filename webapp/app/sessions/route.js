import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    model: function(params) {
        return this.store.query('session', {page: params.page, filter: params.filter});
    }

});
