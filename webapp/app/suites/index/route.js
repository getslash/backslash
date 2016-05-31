import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfiniteScrollRoute from '../../mixins/infinite-scroll-route';


export default Ember.Route.extend(AuthenticatedRouteMixin, InfiniteScrollRoute, {

    titleToken: 'Suites',

    model_name: 'suite',


    queryParams: {
	published: {
	    refreshModel: true,
	},
    },


});
