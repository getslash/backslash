import Ember from 'ember';

export default Ember.ArrayController.extend({
  sortProperties: ['integerId'],
  sortAscending: false,

  queryParams: ["page","perPage"],
  page: 1,
  perPage: 10,
  perPageChanged: function(){
    this.set('page', 1);
  }.observes('perPage'),

  pageBinding: "content.page",
  perPageBinding: "content.perPage",
  totalPagesBinding: "content.totalPages",

  resultsPerPage: [10, 20, 50, 100],

  testStatuses: ['', 'SUCCESS', 'FAILURE', 'ERROR', 'INTERRUPTED', 'RUNNING'],
  metadataQueries: [],

  FilterlogicalID: "",
  FilterTestName: "",
  FilterErrorNum: "",
  FilterFailureNum: "",

  actions: {
    queryTests: function () {
      var arr_simple_params = {};
      if ((typeof this.FilterlogicalID !== "undefined") && (this.FilterlogicalID !== "")) {
        arr_simple_params["logical_id"] = this.FilterlogicalID;
      }
      if ((typeof this.FilterTestName !== "undefined") && (this.FilterTestName !== "")) {
        arr_simple_params["name"] = this.FilterTestName;
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

      if ((typeof this.FilterErrorNum !== "undefined") && (this.FilterErrorNum !== "")) {
        query_params["num_errors"] = 'ge:' + this.FilterErrorNum;
      }

      if ((typeof this.FilterFailureNum !== "undefined") && (this.FilterFailureNum !== "")) {
        query_params["num_failures"] = 'ge:' + this.FilterFailureNum;
      }

      //work on metadata
      this.metadataQueries.forEach(function(metaQuery) {
        if (metaQuery.name !== "")
        {
          if ((metaQuery.type === "Exists") || (metaQuery.queryValue === ""))
          {
            query_params["metadata." + metaQuery.name] = "";
          }
          else
          {
            query_params["metadata." + metaQuery.name] = "eq:" + metaQuery.queryValue;
          }
        }
      });

      if (Object.keys(query_params).length > 0) {
        this.transitionToRoute("search-tests", Ember.$.param( query_params ));
      }
      else
      {
        this.transitionToRoute("tests");
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
      Ember.$("#tests-header").children().removeClass('headerSortDown');
      Ember.$("#tests-header").children().removeClass('headerSortUp');
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
