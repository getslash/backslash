import { helper } from '@ember/component/helper';

export function not(params /*, hash*/) {
  let arg = params[0];
  return !arg;
}

export default helper(not);
