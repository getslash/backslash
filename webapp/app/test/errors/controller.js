import Ember from 'ember';


export default Ember.Controller.extend({

    test: Ember.computed.oneWay('parent_controller.test'),
    session: Ember.computed.oneWay('test.session')
});
