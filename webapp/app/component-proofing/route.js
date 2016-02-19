import Ember from 'ember';

export default Ember.Route.extend({

    model() {
        return {

            traceback_frame: this._generate_traceback_frame(),
            traceback_frame_test_code: this._generate_traceback_frame(true),
        };
    },

    _generate_traceback_frame(is_in_test_code=false) {
        return {
            filename: '/some/path/to/file.py',
            lineno: 666,

            func_name: 'some_func',

            is_in_test_code: is_in_test_code,

            code_string: 'raise Exception("error")',

            locals: {
                local_var1: "Some string",
            },
            globals: {
                global_var1: 120,
            },
        };

    },
});
