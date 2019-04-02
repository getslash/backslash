import { oneWay } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import Component from "@ember/component";

export default Component.extend({
  classNames: ["container-fluid"],
  results: null,
  meta: null,
  show_subjects: true,
  show_users: true,
  session_model: null,
  filter_controller: null,

  display: service(),
});
