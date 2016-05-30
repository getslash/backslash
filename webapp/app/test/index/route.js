import Ember from 'ember';

import BaseRoute from '../../routes/base';
import RefreshableRouteMixin from '../../mixins/refreshable-route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {

    model: function() {
        let test = this.modelFor('test');
        return Ember.RSVP.hash({
            test: test,
            activity: this.store.query('activity', {test_id: test.get('id')}),

            metadata: this.api.call('get_metadata', {
                entity_type: 'test',
                entity_id: parseInt(test.get('id'))
            }).then(r => r.result),
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    }
});
