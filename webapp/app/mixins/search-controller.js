import { observer } from '@ember/object';
import Mixin from '@ember/object/mixin';

export default Mixin.create({

  search: "",
  searching: true,

  clear_search() {
    this.set("search", "");
  },

  clear_page: observer('search', function() {
    this.set('page', 1);
  }),
});
