import Mixin from '@ember/object/mixin';

export default Mixin.create({
  page: 1,
  page_size: 25,

  queryParams: [
    "page",
    "page_size",
  ],

});
