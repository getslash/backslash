import Ember from 'ember';
import DS from 'ember-data';

export default DS.RESTAdapter.extend({
  namespace: 'rest',

  pathForType: function(type) {
      var plural = Ember.String.pluralize(type);
      return Ember.String.underscore(plural);
  },

  ajax: function(url, type, options) {
    return this._super(url, type, options).catch(function(error){
    	error.errors.forEach(function(e){
    	    if (e.status==="404"){ // Replace Ember's default message for 404
                error.not_found = true;
    	    }
    	});
    	throw error;
    });
  },
});
