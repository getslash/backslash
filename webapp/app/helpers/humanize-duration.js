import Ember from 'ember';


function trunc(n) {
    return Number(n.toFixed());
}

export function humanizeDuration(params, hash) {
    if (!hash.end) {
        return '';
    }
    let duration_seconds = hash.end - hash.start;
    let days = trunc(duration_seconds / (24 * 60 * 60));
    duration_seconds %= (24 * 60 * 60);
    let hours = trunc(duration_seconds / (60 * 60));
    duration_seconds %= 60 * 60;
    let minutes = trunc(duration_seconds / 60);
    duration_seconds = trunc(duration_seconds % 60);

    let returned = `${duration_seconds}s`;

    if (hours || minutes) {
        returned = `${minutes}m ${returned}`;
    }
    if (hours || days) {
        returned = `${hours}h ${returned}`;
    }
    if (days) {
        returned = days + 'd ' + returned;
    }
    return returned;
}

export default Ember.Helper.helper(humanizeDuration);
