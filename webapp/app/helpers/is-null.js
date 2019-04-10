import { helper } from "@ember/component/helper";

export function isNull(params /*, hash*/) {
  return params[0] === null;
}

export default helper(isNull);
