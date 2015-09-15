import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../mixins/refreshable-route';

export default BaseRoute.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {

    title: 'Session Details',

    model: function(params) {
        return this.store.find('session', params.id);
    }

});
