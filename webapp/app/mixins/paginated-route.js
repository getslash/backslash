import Mixin from '@ember/object/mixin';

export default Mixin.create({
  queryParams: {
    page: {
      refreshModel: true
    },
    page_size: {
      refreshModel: true
    },
  },

});
