import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({

    archived: DS.attr('boolean'),
    investigated: DS.attr('boolean'),

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),


    num_error_tests: DS.attr('number'),
    num_errors: DS.attr('number'),
    num_failed_tests: DS.attr('number'),
    num_finished_tests: DS.attr('number'),
    num_skipped_tests: DS.attr('number'),
    total_num_tests: DS.attr('number'),

    status: DS.attr('string'),

    subjects: DS.attr(),
    user_email: DS.attr(),

    real_email: DS.attr(),

    is_delegate: Ember.computed.notEmpty('real_email'),

    is_running: function() {
        return this.get('status') === 'RUNNING';
    }.property('status'),

    needs_investigation: function() {
        return this.get('investigated') !== true && this.get('status') !== 'SUCCESS';
    }.property('investigated', 'status'),

    typename: 'session'

});
