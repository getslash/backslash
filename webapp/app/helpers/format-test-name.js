import Ember from 'ember';

export function formatTestName(params, hash) {
    let [info] = params;
    let returned = '';
    if (hash.with_filename === undefined || hash.with_filename) {
	returned += info.file_name + ':';
    }
    if (info.class_name && (info.class_name.indexOf('(') === -1 || info.class_name.endsWith(')'))) {
	returned += info.class_name + '.';
    }
    returned += info.name;
    return returned;
}

export default Ember.Helper.helper(formatTestName);
