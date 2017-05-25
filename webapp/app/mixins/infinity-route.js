import Ember from "ember";

import InfinityRoute from "ember-infinity/mixins/route";

export default Ember.Mixin.create(InfinityRoute, {
  perPageParam: "page_size",
  pageParam: "page",
  totalPagesParam: "meta.pages_total"
});
