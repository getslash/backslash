import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend({

    needs: ['test'],

    model: function(params) {
        return this.store.query('error', {test_id: this.modelFor('test').id, page: params.page});
    }
});
