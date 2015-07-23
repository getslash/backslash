import PaginatedRoute from '../../routes/paginated_route';

export default PaginatedRoute.extend({

    needs: ['session'],

    model: function(params) {
        this.parsePage(params);
        return this.store.query('error', {session_id: this.modelFor('session').id, page: this.get('page')});
    }
});
