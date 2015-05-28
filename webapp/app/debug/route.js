import Ember from 'ember';

export default Ember.Route.extend({
    model: function() {

        return Ember.Object.create({
            session_for_breakdown: Ember.Object.create({
                num_failed_tests: 2,
                num_error_tests: 1,
                num_skipped_tests: 2,
                num_finished_tests: 8,
                is_running: true
            })
        });
    }
});
