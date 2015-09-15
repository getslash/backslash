import Ember from 'ember';

export function not(params/*, hash*/) {

    let arg = params[0];
    return !(arg);

}

export default Ember.Helper.helper(not);
