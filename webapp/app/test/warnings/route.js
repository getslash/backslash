import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend({

    needs: ['test'],

    model: function(params) {
        return this.store.query('warning', {test_id: parseInt(this.modelFor('test').id), page: params.page || 1});
    }
});
