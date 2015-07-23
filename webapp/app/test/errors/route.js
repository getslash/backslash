import PaginatedRoute from '../../routes/paginated_route';

export default PaginatedRoute.extend({

    needs: ['test'],

    model: function(params) {
        this.parsePage(params);
        return this.store.query('error', {test_id: this.modelFor('test').id, page: this.get('page')});
    }
});
