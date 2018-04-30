import { later } from '@ember/runloop';
import $ from 'jquery';
import { inject as service } from '@ember/service';
import Component from '@ember/component';
import { getOwner } from '@ember/application';
import KeyboardShortcuts from "ember-keyboard-shortcuts/mixins/component";
import { timeout, task } from "ember-concurrency";

let _keys = [
  { key: ".", action: "open_quick_search", description: "Opens quick jump" },
  {
    key: "h",
    action: "toggle_human_times",
    description: "Toggles human-readable times"
  },
  { key: "a", action: "filter_none", description: "Show all entities" },
  {
    key: "f",
    action: "filter_only_failed",
    description: "Hide all entities except failed"
  },
  {
    key: "c",
    action: "toggle_inline_comment",
    description: "Toggle comment preview for items"
  },
  {
    key: "s",
    action: "toggle_session_side_labels",
    description: "Toggle the side breakdown panel for Sessions"
  },
  { key: "j", action: "jump_one_down", description: "Jump to next item" },
  { key: "k", action: "jump_one_up", description: "Jump to previous item" },

  { key: "u", action: "goto_session_tests", description: "Go back to session's test list" },

  { key: "esc", action: "close_boxes_or_home" },
  {
    key: "ctrl+s",
    action: "goto_sessions",
    description: "Jump to Sessions view"
  },
  { key: "ctrl+u", action: "goto_users", description: "Jump to Users view" },
  { key: "?", action: "display_help", description: "Show this help message" }
];

let _shortcuts = {};

_keys.forEach(function(k) {
  _shortcuts[k.key] = {
    action: k.action,
    global: false
  };
});

let _FILTERABLE_VIEWS = [
  "sessions",
  "session.index",
  "user.sessions",
  "subject",
  "test_info"
];

export default Component.extend(KeyboardShortcuts, {
  help_displayed: false,

  keyboardShortcuts: _shortcuts,
  keys: _keys,

  api: service(),
  display: service(),
  store: service(),

  search(query, sync_callback, async_callback) {
    this.get("async_search").perform(query, async_callback);
  },

  select(obj) {
    let self = this;

    self.sendAction("close_boxes");
    self._close_boxes();
    self.router.transitionTo(obj.route, obj.key);
  },

  async_search: task(function*(query, callback) {
    yield timeout(400);
    let res = yield this.get("api").call("quick_search", { term: query });
    res = res.result;
    if (res.length === 0) {
      res.push({
        type: "session",
        name: "Go to session " + query,
        key: query,
        route: "session"
      });
      res.push({
        type: "test",
        name: "Go to test " + query,
        key: query,
        route: "test"
      });
    }
    callback(res);
  }).restartable(),

  _close_boxes() {
    let element = $("#goto-input");
    element.typeahead("destroy");
    element.off();
    this.set("quick_search_open", false);
    this.get("display").set("show_help", false);
  },

  _do_if_in(paths, callback) {
    let approute = getOwner(this).lookup("route:application");
    let appcontroller = getOwner(this).lookup("controller:application");
    let path = appcontroller.currentPath;
    if (paths.indexOf(path) !== -1) {
      let controller = approute.controllerFor(path);
      callback(controller);
    }
  },

  jump_one(direction) {
    let self = this;
    let appcontroller = getOwner(this).lookup("controller:application");
    let current_path = appcontroller.currentPath;

    if (!current_path.startsWith("session.test.")) {
      return;
    }

    let session_controller = getOwner(this).lookup("controller:session");
    let test = session_controller.get("current_test");
    let session = session_controller.get("session_model");
    console.assert(session_controller); // eslint-disable-line no-console
    console.assert(test); // eslint-disable-line no-console
    let session_id = test.get("session_id");
    if (session.get('child_id') !== null) {
      session_id = session.get('parent_logical_id')
    }
    let filters = { session_id: session_id };
    filters[direction + "_index"] = test.get("test_index");

    Object.assign(filters, session_controller.get("test_filters"));

    self.get("store").queryRecord("test", filters).then(function(test) {
      if (test) {
        self.router.transitionTo(
          current_path,
          session.get("display_id"),
          test.get("display_id")
        );
      }
    });
  },

  actions: {
    toggle_session_side_labels() {
      this.get("display").toggleProperty("show_side_labels");
    },

    close_box() {
      this._close_boxes();
    },

    close_boxes_or_home() {
      if (this.get("quick_search_open") ||  this.get("display.show_help")) {
        this._close_boxes();
      } else {
        this._do_if_in(["sessions", "session.index"], function(controller) {
          controller.clear_search();
        });
        this.router.transitionTo(this.router.currentPath);
      }
    },

    display_help() {
      this.get("display").set('show_help', true);
    },

    goto_sessions() {
      this.router.transitionTo("sessions");
    },

    goto_users() {
      this.router.transitionTo("users");
    },

    goto_session_tests() {
      let appcontroller = getOwner(this).lookup("controller:application");
      let current_path = appcontroller.currentPath;

      if (!current_path.startsWith("session.test.")) {
        return;
      }

      let session_controller = getOwner(this).lookup("controller:session");
      let session = session_controller.get("session_model");
      this.router.transitionTo("session.index", session.get('display_id'));
    },

    toggle_human_times() {
      this.get("display").toggleProperty("humanize_times");
    },

    filter_only_failed() {
      this._do_if_in(_FILTERABLE_VIEWS, function(controller) {
        controller.filter_all_except("unsuccessful");
      });
    },

    filter_none() {
      this._do_if_in(_FILTERABLE_VIEWS, function(controller) {
        controller.filter_none_except("planned");
      });
    },

    toggle_inline_comment() {
      this.get("display").toggleProperty("comments_expanded");
    },

    open_quick_search() {
      let self = this;
      self.set("quick_search_open", true);
      later(function() {
        let element = $("#goto-input");
        element.typeahead(
          {
            hint: true,
            highlight: true,
            minLength: 1
          },
          {
            name: "Suggestions",
            source: self.search.bind(self),
            display: "name",
            templates: {
              suggestion: function(obj) {
                let icon;
                if (obj.type === "subject") {
                  icon = "rocket";
                } else if (obj.type === "user") {
                  icon = "user";
                }

                return `<div><i class="fa fa-${icon}"></i> ${obj.name}</div>`;
              }
            }
          }
        );
        element
          .on("keyup", function(e) {
            if (e.keyCode === 27) {
              self._close_boxes();
            }
          })
          .on("typeahead:selected", function(evt, obj) {
            self.select(obj);
          })
          .on("typeahead:render", function() {
            element.parent().find(".tt-selectable:first").addClass("tt-cursor");
          })
          .focus();
      });
    },

    jump_one_down() {
      this.jump_one("before");
    },

    jump_one_up() {
      this.jump_one("after");
    }
  }
});
