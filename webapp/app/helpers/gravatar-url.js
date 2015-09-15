import Ember from 'ember';

export function gravatarUrl(params/*, hash*/) {

    let email = params[0];
    return 'http://www.gravatar.com/avatar/' + window.md5(email);

}

export default Ember.Helper.helper(gravatarUrl);
