import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {
  model: function() {
        return {features: [
            {name: "Font Awesome", ok: true},
            {name: "Ember.js", ok: true},
            {name: "Bootstrap", ok: true}
        ]};
    }
});
