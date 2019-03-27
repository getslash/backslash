import $ from "jquery";
import { later } from "@ember/runloop";
import Component from "@ember/component";
import { timeout, task } from "ember-concurrency";
import { inject as service } from "@ember/service";

export default Component.extend({
  tagName: "form",
  classNames: "form-inline w-100",
  api: service(),

  async_search: task(function*(query, callback) {
    yield timeout(400);
    let res = yield this.get("api").call("quick_search", { term: query });
    res = res.result;
    if (res.length === 0) {
      res.push({
        type: "session",
        name: "Go to session " + query,
        key: query,
        route: "session",
      });
      res.push({
        type: "test",
        name: "Go to test " + query,
        key: query,
        route: "test",
      });
    }
    callback(res);
  }).restartable(),

  search(query, sync_callback, async_callback) {
    this.get("async_search").perform(query, async_callback);
  },

  select(obj) {
    let self = this;
    self.router.transitionTo(obj.route, obj.key);
  },

  didInsertElement() {
    let self = this;
    later(function() {
      let element = $("#quick-search-input");
      element.blur();
      let nav_container = element.closest("ul");
      element.typeahead(
        {
          hint: true,
          highlight: true,
          minLength: 1,
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
            },
          },
        }
      );
      element
        .on("typeahead:selected", function(evt, obj) {
          self.select(obj);
        })
        .on("focusin", function() {
          nav_container.addClass("flex-grow-1");
          nav_container.removeClass("flex-grow-0");
        })
        .on("focusout", function() {
          nav_container.addClass("flex-grow-0");
          nav_container.removeClass("flex-grow-1");
        })
        .on("typeahead:render", function() {
          element
            .parent()
            .find(".tt-selectable:first")
            .addClass("tt-cursor");
        });
    });
  },
});
