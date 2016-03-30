import Ember from 'ember';

import PaginatedFilteredController from '../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({

    collection: Ember.computed.oneWay('sessions'),

    queryParams: ['humanize_times', 'show_successful', 'show_unsuccessful', 'show_abandoned', 'show_skipped'],

    humanize_times: true,
    show_successful: true,
    show_unsuccessful: true,
    show_abandoned: true,
    show_skipped: true,

});
