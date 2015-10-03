import DS from 'ember-data';

export default DS.Model.extend({

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),
    duration: DS.attr('number'),
    status: DS.attr('string'),
    name: DS.attr('string'),
    num_errors: DS.attr('number'),
    num_warnings: DS.attr('number'),

    scm: DS.attr(),
    scm_revision: DS.attr(),
    scm_dirty: DS.attr(),
    file_hash: DS.attr(),

    skip_reason: DS.attr(),

    info: DS.attr(),
    session_id: DS.attr('number'),

    is_success: function() {
        return (this.get('status') === 'SUCCESS');
    }.property('status'),

    is_skipped: function() {
        return (this.get('status') === 'SKIPPED');
    }.property('status'),


    is_running: function() {
        return this.get('status') === 'RUNNING';
    }.property('status')

});
