import Mixin from '@ember/object/mixin';

export default Mixin.create({
  actions: {
    refreshRoute: function() {
      this.refresh();
    }
  }
});
