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
  resultsPerPage: [10, 20, 50, 100],
  FilterlogicalID: "",
  FilterUserName: "",
  FilterProductName: "",
  FilterProductVersion: "",
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
      if ((typeof this.FilterlogicalID !== "undefined") && (this.FilterlogicalID !== "")) {
        arr_simple_params["logical_id"] = this.FilterlogicalID;
      }
      if ((typeof this.FilterUserName !== "undefined") && (this.FilterUserName !== "")) {
        arr_simple_params["user_name"] = this.FilterUserName;
      }
      if ((typeof this.FilterProductName !== "undefined") && (this.FilterProductName !== "")) {
        arr_simple_params["product_name"] = this.FilterProductName;
      }
      if ((typeof this.FilterProductVersion !== "undefined") && (this.FilterProductVersion !== "")) {
        arr_simple_params["product_version"] = this.FilterProductVersion;
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
      var header_name;
      if (property === "") //just refresh on init
      {
        var properties_array = this.get('sortProperties');
        header_name = "#header-" + properties_array[0];
      }
      else
      {
        this.set('sortProperties', [property]);
        this.set('sortAscending', !this.get('sortAscending'));
        header_name = "#header-" + property;
      }
      Ember.$("#sessions-header").children().removeClass('headerSortDown');
      Ember.$("#sessions-header").children().removeClass('headerSortUp');
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
