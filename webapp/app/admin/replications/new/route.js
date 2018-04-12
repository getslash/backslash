import Object from '@ember/object';
import Route from '@ember/routing/route';

export default Route.extend({

    model() {
        return this.store.createRecord('replication');
    },

    resetController(controller) {
        if (controller.get('model.isNew')) {
            controller.get('model').destroyRecord();
        }
    },
});
