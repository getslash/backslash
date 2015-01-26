import Ember from 'ember';
import RouteMixin from 'ember-cli-pagination/remote/route-mixin';

Ember.$.extend({

  getQueryParameters : function(str) {
    return (str).replace(/(^\?)/,'').split("&").map(function(n){return n = n.split("="),this[n[0]] = decodeURIComponent(n[1]),this;}.bind({}))[0];
  }

});

export default Ember.Route.extend(RouteMixin, {
  model: function(params) {
    var new_params = Ember.$.getQueryParameters(params.filters);
    new_params.paramMapping = {page: "page",
      perPage: "page_size",
      total_pages: "total_num_pages"};
    var paged = this.findPaged('test', new_params);
    paged.fromGeneralTestsTable = true;
    return paged;
  },
  controllerName: 'tests',

  renderTemplate: function() {
    this.render('tests');
  }
});
