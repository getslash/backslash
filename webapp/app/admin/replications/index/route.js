import Route from '@ember/routing/route';
import {hash} from 'rsvp';
import PollingRoute from "../../../mixins/polling-route";

export default Route.extend(PollingRoute, {
    INTERVAL_SECONDS: 5,

    should_auto_refresh() {
        return true;
    },

    model() {
        return hash({
            replications: this.store.findAll('replication', {reload: true}),
        });
    },

    setupController(controller, model) {
        this._super(...arguments);
        controller.setProperties(model);
    },

});
