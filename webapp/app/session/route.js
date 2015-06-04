import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {

    title: 'Session Details',

    model: function(params) {
        return this.store.find('session', params.id);
    },

});
