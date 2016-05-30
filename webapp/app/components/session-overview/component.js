import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['container-fluid'],
    show_breakdown: true,
    session_model: null,
    user: null,

    not_complete: Ember.computed.and('session_model.finished_running', 'session_model.has_tests_left_to_run'),
});
