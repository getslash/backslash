import Ember from 'ember';


export default Ember.Controller.extend({

    test: Ember.computed.alias('parent_controller.test')
});
