import Ember from 'ember';

export default Ember.Route.extend({

    activate() {
        let c = this.controllerFor('application');
        c.set('loading', true);
    }
});
