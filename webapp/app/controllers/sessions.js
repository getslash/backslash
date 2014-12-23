import Ember from 'ember';

export default Ember.ArrayController.extend({
  showRunning: false,
  selectedStatus: null,
  sortProperties: ['nId'],
  sortAscending: false,
  filteredSessions: function() {
    var sessions = this.get('arrangedContent');

    if (!sessions || !this.get('showRunning')) {
      return sessions;
    }

    return sessions.filter(function(item) {
      return item.get('isRunning');
    });
  }.property('showRunning','arrangedContent', 'model.[]'),

  sessionStatuses: ['', 'SUCCESS', 'FAILURE', 'RUNNING'],
  actions: {
    querySessions: function () {
      var arr_simple_params = {};
      if ((typeof FilterlogicalID !== "undefined") && (FilterlogicalID !== "")) {
        arr_simple_params["logical_id"] = FilterlogicalID;
      }
      if ((typeof FilterUserName !== "undefined") && (FilterUserName !== "")) {
        arr_simple_params["user_name"] = FilterUserName;
      }
      if ((typeof FilterProductName !== "undefined") && (FilterProductName !== "")) {
        arr_simple_params["product_name"] = FilterProductName;
      }
      if ((typeof FilterProductVersion !== "undefined") && (FilterProductVersion !== "")) {
        arr_simple_params["product_version"] = FilterProductVersion;
      }

      var query = "";
      var not_first_param = false;
      for (var key in arr_simple_params) {
        if (arr_simple_params.hasOwnProperty(key)) {
          if (arr_simple_params[key]) {
            if (not_first_param) {
              query += "&";
            }
            query += key + '=' + encodeURIComponent(arr_simple_params[key]);
            not_first_param = true;
          }
        }
      }

      if (this.selectedStatus !== "") {
        if (not_first_param) {
          query += "&";
        }
        query += 'status=' + this.selectedStatus;
        not_first_param = true;
      }

      this.transitionToRoute("search-sessions", query);
    },
    sortBy: function(property) {
      this.set('sortProperties', [property]);
      this.set('sortAscending', !this.get('sortAscending'));
      Ember.$("#sessions-header").children().removeClass('headerSortDown');
      Ember.$("#sessions-header").children().removeClass('headerSortUp');
      var header_name = "#header-" + property;
      if (this.get('sortAscending'))
      {
        Ember.$(header_name).addClass('headerSortDown');
      }
      else
      {
        Ember.$(header_name).addClass('headerSortUp');
      }
    }

  }

});
