import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfinityRoute from 'ember-infinity/mixins/route';


export default Ember.Route.extend(AuthenticatedRouteMixin, InfinityRoute, {

    titleToken: 'Users',

    perPageParam: "page_size",
    pageParam: "page",
    totalPagesParam: "meta.pages_total",

    queryParams: {
        sort: {
            refreshModel: true,
        },
    },

    model(params) {
	let sort_order = params.sort;

        return Ember.RSVP.hash({
            users: this.infinityModel(
                "user",
                {perPage: 50, startingPage: 1, modelPath: 'controller.users', sort: sort_order}),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },
});
