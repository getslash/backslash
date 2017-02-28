import Ember from 'ember';
import PaginatedFilteredController from '../../controllers/paginated_filtered_controller';
import StatusFilterableController from '../../mixins/status-filterable/controller';

import config from '../../config/environment';

export default PaginatedFilteredController.extend(StatusFilterableController, {

    queryParams: ['show_planned'],
    show_planned: false,

    collection: Ember.computed.oneWay('tests'),

    available_page_sizes: config.APP.available_page_sizes,

    display: Ember.inject.service(),
});
