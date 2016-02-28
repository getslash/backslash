import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    model() {
        return this.api.call('get_admin_stats').then(function(result) {
            let res = result.result;
            let max = res.load_avg.gauge.max;
            res.load_avg.gauge.label.format = function(avg) {
                return avg.toFixed(2);
            };

            res.load_avg.color = {
                pattern: ['green', 'orange', 'red'], // the three color levels for the percentage values.
                unit: 'value',
                threshold: {
                    values: [max * 0.5, max * 0.8]
                }
            };


            return res;
        });
    }
});
