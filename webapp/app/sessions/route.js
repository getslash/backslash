import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {

    title: 'Sessions',

    model: function() {

        return this.store.query('session', {page: 1});
    }

});
