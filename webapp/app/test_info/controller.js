import Ember from 'ember';

import PaginatedFilteredController from '../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({
    page: 1,

    collection: Ember.computed.oneWay('tests'),
});
