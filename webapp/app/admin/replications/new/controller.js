import Controller from '@ember/controller';
import { inject as service } from "@ember/service";

export default Controller.extend({

    actions: {
        save() {
            let self = this;
            self.get('model').save().then(function() {
                self.router.transitionTo('admin.replications.index');
            });
        },
    },
});
