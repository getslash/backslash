import Ember from 'ember';


export default Ember.Controller.extend({

    single_error_route_name: 'session.single_error',

    parent_id: Ember.computed.oneWay('session.id')
});
