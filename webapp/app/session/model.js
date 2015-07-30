import DS from 'ember-data';

export default DS.Model.extend({

    archived: DS.attr('boolean'),

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),
    status: DS.attr('string'),

    total_num_tests: DS.attr('number'),
    num_failed_tests: DS.attr('number'),
    num_error_tests: DS.attr('number'),
    num_skipped_tests: DS.attr('number'),
    num_finished_tests: DS.attr('number'),

    num_errors: DS.attr('number'),

    user_email: DS.attr(),

    subjects: DS.attr(),

    is_running: function() {
        return this.get('status') === 'RUNNING';
    }.property('status'),


    typename: 'session'

});
