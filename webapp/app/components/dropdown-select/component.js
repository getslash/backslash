import Component from '@ember/component';

export default Component.extend({
  value: null,
  title: null,
  options: [],

  actions: {
    select(item) {
      this.set("value", item);
    }
  }
});
