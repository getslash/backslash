import Ember from 'ember';

import PaginatedFilteredController from '../controllers/paginated_filtered_controller';
import StatusFilterableController from '../mixins/status-filterable/controller';

export default PaginatedFilteredController.extend(StatusFilterableController, {
    page: 1,

    collection: Ember.computed.oneWay('tests'),
});
