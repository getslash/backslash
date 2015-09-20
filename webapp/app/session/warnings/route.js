import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend({

    needs: ['session'],

    model: function(params) {
        return this.store.query('warning', {session_id: parseInt(this.modelFor('session').id), page: params.page || 1});
    }
});
