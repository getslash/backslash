import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfinityRoute from 'ember-infinity/mixins/route';


export default Ember.Route.extend(AuthenticatedRouteMixin, InfinityRoute, {

    titleToken: 'Subjects',

    perPageParam: "page_size",
    pageParam: "page",
    totalPagesParam: "meta.pages_total",

    queryParams: {
        sort: {
            refreshModel: true,
        },
    },

    model(params) {
        return Ember.RSVP.hash({
            subjects: this.infinityModel(
                "subject",
                {perPage: 50, startingPage: 1, modelPath: 'controller.subjects', sort: params.sort}),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },
});
