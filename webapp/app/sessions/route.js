import PaginatedRoute from '../routes/paginated_route';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default PaginatedRoute.extend(AuthenticatedRouteMixin, {

    title: 'Sessions',

    model: function(params) {
        this.parsePage(params);
        return this.store.query('session', {page: this.get('page')});
    }

});
