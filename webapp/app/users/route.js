import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {
    model: function(params) {
        this.store.unloadAll();
        return this.store.query('user', {page: params.page});
    }
});
