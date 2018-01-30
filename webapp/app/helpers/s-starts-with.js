import Ember from "ember";

export function sStartsWith(params /*, hash*/) {
    let [s, ...prefixes] = params;
    for (let prefix of prefixes) {
        if (s.startsWith(prefix)) {
            return true;
        }
    }
    return false;
}

export default Ember.Helper.helper(sStartsWith);
