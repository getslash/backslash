import Mixin from '@ember/object/mixin';

import InfinityRoute from "ember-infinity/mixins/route";

export default Mixin.create(InfinityRoute, {
  perPageParam: "page_size",
  pageParam: "page",
  totalPagesParam: "meta.pages_total"
});
