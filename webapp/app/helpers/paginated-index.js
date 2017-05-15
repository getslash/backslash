import Ember from "ember";

export function paginatedEach(params) {
  let index = params[0];
  let page = params[1];
  let page_size = params[2];

  return (page - 1) * page_size + index + 1;
}

export default Ember.Helper.helper(paginatedEach);
