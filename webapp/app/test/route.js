import BaseRoute from '../routes/base';

export default BaseRoute.extend({

    title: 'Test Details',

    model: function(params) {
        return this.store.find('test', params.test_id);
    }
});
