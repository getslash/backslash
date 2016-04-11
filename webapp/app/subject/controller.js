import Ember from 'ember';

import PaginatedFilteredController from '../controllers/paginated_filtered_controller';
import StatusFilterableController from '../mixins/status-filterable/controller';

export default PaginatedFilteredController.extend(StatusFilterableController, {
    collection: Ember.computed.oneWay('sessions'),
});
