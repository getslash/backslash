import PaginatedFilteredController from '../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({
    actions: {
        goto_subject(subject) {
            this.transitionToRoute('subject', subject.get('name'));
        },
    },
});
