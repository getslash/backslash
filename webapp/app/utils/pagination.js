import Object from '@ember/object';

export default Object.reopenClass({

  ALL_FILTERS: [
    "show_successful",
    "show_unsuccessful",
    "show_abandoned",
    "show_skipped",
  ],

  get_defaults() {
    return {
      show_successful: true,
      show_unsuccessful: true,
      show_abandoned: true,
      show_skipped: true,
    };
  },
});
