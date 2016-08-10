import Ember from 'ember';

export function sStartsWith(params/*, hash*/) {
    let [s, prefix] = params;
    return s.startsWith(prefix);
}

export default Ember.Helper.helper(sStartsWith);
