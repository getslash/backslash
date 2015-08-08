import PaginatedFilteredController from '../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({

    queryParams: ['show_archived'],
    show_archived: false,

    actions: {
        toggle_show_archived: function() {
            this.set('show_archived', !this.get('show_archived'));
        }
    }

});
