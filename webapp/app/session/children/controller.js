import Ember from 'ember';


export default Ember.Controller.extend({
    sortProperties: ['child_id:asc'],
    sortedModel: Ember.computed.sort('children', 'sortProperties'),
});
