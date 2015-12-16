import PaginatedFilteredController from '../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({

    queryParams: ['sort'],

    sort: 'email',

    actions: {

        set_sort(field_name) {
            this.set('sort', field_name);
        },
    },

});
