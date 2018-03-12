import { helper } from '@ember/component/helper';

export function undasherize(params /*, hash*/) {
  return params[0].replace(/_/g, " ");
}

export default helper(undasherize);
