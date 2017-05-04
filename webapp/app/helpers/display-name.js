import Ember from 'ember';

export default Ember.Helper.extend({

    runtime_config: Ember.inject.service(),

    compute(params/*, hash*/) {
        let cached = this.get('runtime_config').get_cached(`display_names.${params[0]}`);
        return cached;
    },
});
