import { oneWay } from '@ember/object/computed';
import Controller from '@ember/controller';

export default Controller.extend({
  single_error_route_name: "session.single_error",

  parent_id: oneWay("session.id")
});
