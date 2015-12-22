import DS from 'ember-data';
import HasLogicalId from '../mixins/has-logical-id';

export default DS.Model.extend(HasLogicalId, {

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),
    duration: DS.attr('number'),
    status: DS.attr('string'),
    num_errors: DS.attr('number'),
    num_warnings: DS.attr('number'),

    test_info_id: DS.attr('number'),

    type: DS.attr(),

    first_error: DS.attr(),

    scm: DS.attr(),
    scm_revision: DS.attr(),
    scm_dirty: DS.attr(),
    file_hash: DS.attr(),

    skip_reason: DS.attr(),

    info: DS.attr(),
    session_id: DS.attr('number'),

    variation: DS.attr(),

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
