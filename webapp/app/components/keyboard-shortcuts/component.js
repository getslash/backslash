import $ from "jquery";
import { inject as service } from "@ember/service";
import Component from "@ember/component";
import { getOwner } from "@ember/application";
import { bindKeyboardShortcuts } from "ember-keyboard-shortcuts";

let _keys = [
  {
    key: ".",
    action: "focus_quick_search",
    description: "Focus quick search box",
  },
  {
    key: "h",
    action: "toggle_human_times",
    description: "Toggles human-readable times",
  },
  {
    key: "c",
    action: "toggle_compact_view",
    description: "Toggles compact view where available",
  },
  { key: "a", action: "filter_none", description: "Show all entities" },
  {
    key: "f",
    action: "filter_only_failed",
    description: "Hide all entities except failed",
  },
  { key: "j", action: "jump_one_down", description: "Jump to next item" },
  { key: "k", action: "jump_one_up", description: "Jump to previous item" },
  {
    key: "o",
    action: "toggle_session_overview",
    description: "Toggle session overview when looking at tests",
  },
  {
    key: "u",
    action: "goto_session_tests",
    description: "Go back to session's test list",
  },

  { key: "esc", action: "close_boxes_or_home" },
  {
    key: "ctrl+s",
    action: "goto_sessions",
    description: "Jump to Sessions view",
  },
  { key: "ctrl+u", action: "goto_users", description: "Jump to Users view" },
  { key: "?", action: "display_help", description: "Show this help message" },
];

let _shortcuts = {};

_keys.forEach(function(k) {
  _shortcuts[k.key] = {
    action: k.action,
    global: false,
  };
});

let _FILTERABLE_VIEWS = [
  "sessions",
  "session.index",
  "user.sessions",
  "subject",
  "test_info",
];

export default Component.extend({
  help_displayed: false,

  keyboardShortcuts: _shortcuts,
  keys: _keys,

  display: service(),
  store: service(),
  router: service(),

  didInsertElement() {
    bindKeyboardShortcuts(this);
  },

  _close_boxes() {
    this.get("display").set("show_help", false);
    this.set("help_displayed", false);
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
    if (session.get("child_id") !== null) {
      session_id = session.get("parent_logical_id");
    }
    let filters = { session_id: session_id };
    filters[direction + "_index"] = test.get("test_index");

    Object.assign(filters, session_controller.get("test_filters"));

    self
      .get("store")
      .queryRecord("test", filters)
      .then(function(test) {
        if (test) {
          return self.router.transitionTo(
            current_path,
            test.get("session_display_id"),
            test.get("display_id")
          );
        }
      });
  },

  actions: {
    close_box() {
      this._close_boxes();
    },

    close_boxes_or_home() {
      if (this.get("display.show_help") || this.get("help_displayed")) {
        this._close_boxes();
      } else {
        this._do_if_in(["sessions", "session.index"], function(controller) {
          controller.clear_search();
        });
        this.router.transitionTo(this.router.currentPath);
      }
    },

    display_help() {
      this.toggleProperty("help_displayed");
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

      if (!current_path.startsWith("session.")) {
        return;
      }

      let session_controller = getOwner(this).lookup("controller:session");
      let session = session_controller.get("session_model");
      this.router.transitionTo("session.index", session.get("display_id"));
    },

    toggle_human_times() {
      this.get("display").toggleProperty("humanize_times");
    },

    toggle_compact_view() {
      let approute = getOwner(this).lookup("route:application");
      let appcontroller = getOwner(this).lookup("controller:application");
      let path = appcontroller.currentPath;
      let controller = approute.controllerFor(path);
      if (controller.get("compact_view") !== undefined) {
        controller.toggleProperty("compact_view");
      }
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

    focus_quick_search() {
      $("#quick-search-input").focus();
    },

    jump_one_down() {
      this.jump_one("before");
    },

    jump_one_up() {
      this.jump_one("after");
    },

    toggle_session_overview() {
      const owner = getOwner(this);
      let appcontroller = owner.lookup("controller:application");
      let current_route = appcontroller.currentPath;
      if (current_route.startsWith("session.test.")) {
        let controller = owner.lookup("controller:session.test");
        controller.toggleProperty("show_session_overview");
      }
    },
  },
});
