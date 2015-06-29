import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {

    title: 'Test Details',

    model: function(params) {
        return this.store.find('test', params.test_id);
    }
});
