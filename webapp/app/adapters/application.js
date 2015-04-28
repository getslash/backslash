import Ember from 'ember';
import DS from 'ember-data';

export default DS.RESTAdapter.extend({
  namespace: 'rest',
  pathForType: function(type) {
    var plural = Ember.String.pluralize(type);
    return Ember.String.underscore(plural);
  }
});
