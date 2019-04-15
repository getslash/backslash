import { helper } from "@ember/component/helper";

export function exists(params /*, hash*/) {
  let arg = params[0];
  return arg !== null && arg !== undefined;
}

export default helper(exists);
