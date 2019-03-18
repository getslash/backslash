import Service from "@ember/service";
import { computed } from "@ember/object";

const _DEFAULTS = {
  humanize_times: true,
  comments_expanded: false,
  show_side_labels: false,
  show_help: false,
  session_side_bar_collapsed: false,
  show_avatars: false,
};

let _classvars = {};

let _setting = computed({
  set(key, value) {
    localStorage.setItem("display." + key, value === true);
    this.set("_cache_" + key, value);
    return value;
  },

  get(key) {
    let value = this.get("_cache_" + key);

    if (value !== undefined) {
      return value;
    }

    value = localStorage.getItem("display." + key);
    if (value !== "true" && value !== "false") {
      return _DEFAULTS[key];
    }
    return value === "true";
  },
});

for (let field_name in _DEFAULTS) {
  if (_DEFAULTS.hasOwnProperty(field_name)) {
    _classvars[field_name] = _setting;
  }
}

export default Service.extend(_classvars);
