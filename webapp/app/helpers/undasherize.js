import Ember from 'ember';

export function undasherize(params/*, hash*/) {
  return params[0].replace("_", " ");
}

export default Ember.Helper.helper(undasherize);
