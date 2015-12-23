import Ember from 'ember';

export default Ember.Route.extend({

    model() {
        return this.api.call('get_admin_stats').then(r => r.result);
    }
});
