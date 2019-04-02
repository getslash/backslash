import { computed } from "@ember/object";

export function lower_case(dependent_key) {
  return computed(dependent_key, function() {
    let returned = this.get(dependent_key);
    if (returned) {
      returned = returned.toLowerCase();
    }
    return returned;
  });
}
