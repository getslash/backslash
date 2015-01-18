import Ember from 'ember';

export default Ember.ArrayController.extend({
  queryParams: ["page","perPage"],
  page: 1,
  perPage: 10,
  perPageChanged: function(){
    this.set('page', 1);
  }.observes('perPage'),

  pageBinding: "content.page",
  perPageBinding: "content.perPage",
  totalPagesBinding: "content.totalPages",

  showRunning: false,
  selectedStatus: null,
  sortProperties: ['integerId'],
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
  resultsPerPage: [10, 20, 50, 100],
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

      var query_params = {};
      for (var key in arr_simple_params) {
        if (arr_simple_params.hasOwnProperty(key)) {
          if (arr_simple_params[key]) {
            query_params[key] = 'contains:' + encodeURIComponent(arr_simple_params[key]);
          }
        }
      }

      if (this.selectedStatus !== "") {
        query_params['status'] = this.selectedStatus;
      }

      if ((this.queryStartDate !== undefined) && (this.queryStartDate !== null))
      {
        var momentDate = moment(this.queryStartDate, "DD-MM-YYYY");
        query_params['start_time'] = 'gt:' + momentDate.unix();
      }

      if (Object.keys(query_params).length > 0) {
        this.transitionToRoute("search-sessions", Ember.$.param( query_params ));
      }
      else
      {
        this.transitionToRoute("sessions");
      }
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
