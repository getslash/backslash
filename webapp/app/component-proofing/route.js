import Ember from 'ember';

export default Ember.Route.extend({

    model() {
        return Ember.Object.create({

            traceback_frame: this._generate_traceback_frame(),

            session_result: this._create_session_result(),

        });
    },

    _create_session_result() {
        return Ember.Object.create({
            type: 'session',
            start_time: 198383983,
            end_time: 198383983,
            total_num_tests: 50,
            num_failed_tests: 0,
            num_error_tests: 1,
            num_skipped_tests: 9,
            num_finished_tests: 50,

            num_errors: 0,
            total_num_warnings: 10,

            is_abandoned: false,

            user_email: 'vmalloc@gmail.com',
        });
    },

    _generate_traceback_frame() {
        return Ember.Object.create({
            filename: '/some/path/to/file.py',
            lineno: 666,

            func_name: 'some_func',

            is_in_test_code: false,

            code_string: 'raise Exception("error")',

            locals: {
                local_var1: "Some string",
            },
            globals: {
                global_var1: 120,
            },
        });

    },
});
