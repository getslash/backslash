import EmberObject from '@ember/object';
import Route from '@ember/routing/route';

import HasComputedStatus from "../mixins/has-computed-status";

export default Route.extend({
  model() {
    return EmberObject.create({
      traceback_frame: this._generate_traceback_frame(),

      session_result: this._create_session_result(),

      test_result: this._create_test_result()
    });
  },

  _create_session_result() {
    return EmberObject
      .extend(HasComputedStatus, {
        num_successful_tests: function() {
          return (
            this.get("num_finished_tests") -
            this.get("num_error_tests") -
            this.get("num_failed_tests") -
            this.get("num_skipped_tests")
          );
        }.property(
          "num_finished_tests",
          "num_error_tests",
          "num_failed_tests",
          "num_skipped_tests"
        )
      })
      .create({
        type: "session",
        start_time: 1457385114.678091,
        end_time: 1457385814.678091,
        total_num_tests: 50,
        num_failed_tests: 0,
        num_error_tests: 1,
        num_skipped_tests: 9,
        num_finished_tests: 50,

        status: "failed",

        num_errors: 0,
        total_num_warnings: 10,

        is_abandoned: false,

        user_email: "vmalloc@gmail.com",
        user_display_name: "Rotem Yaari",

        subjects: [
          {
            name: "micro01",
            product: "MicroWave",
            revision: "c956b18987c06a9f1f66c7a6dea6f68e9e771cc1",
            version: "3.0.0.1-dev"
          },
          {
            name: "micro02",
            product: "MicroWave",
            revision: "c956b18987c06a9f1f66c7a6dea6f68e9e771cc1",
            version: "2.0"
          }
        ]
      });
  },

  _create_test_result() {
    let cls = EmberObject.extend(HasComputedStatus, {
      first_error: function() {
        let status = this.get("status");
        if (status === "error" || status === "failure") {
          return {
            exception_type: "OSError",
            message: "No such file or directory: /very/long/filename/here/should/be/hidden"
          };
        }
        return null;
      }.property("status"),

      num_errors: function() {
        let status = this.get("status");
        if (status === "error" || status === "failure") {
          return 20;
        }
        return 0;
      }.property("status"),

      skip_reason: function() {
        if (this.get("status") === "skipped") {
          return "Test cannot run now";
        }
        return null;
      }.property("status")
    });
    let returned = cls.create({
      type: "test",
      info: {
        file_name: "some/file/name.py",
        name: "test_something_very_long_test_name_that_takes_most_space"
      },
      status: "failure",
      start_time: 1457385114.678091,
      end_time: 1457385314.678091,
      duration: 239,
      num_comments: 0,
      variation: {
        param1: 205,
        param2: "something",
        param3: "something_very_long_here"
      }
    });

    return returned;
  },

  _generate_traceback_frame() {
    return EmberObject.create({
      filename: "/some/path/to/file.py",
      lineno: 666,

      func_name: "some_func",

      is_in_test_code: false,

      code_string: 'raise Exception("error")',

      locals: null,
      globals: null
    });
  }
});
