import DS from 'ember-data';

export default DS.Model.extend({

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),
    status: DS.attr('string'),

    num_failed_tests: DS.attr('number'),
    num_error_tests: DS.attr('number'),
    num_skipped_tests: DS.attr('number'),
    num_finished_tests: DS.attr('number'),

    is_running: function() {
        return this.get('status') === 'RUNNING';
    }.property('status')


});
