import { reject, hash } from 'rsvp';
import { inject as service } from '@ember/service';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
from "ember-simple-auth/mixins/authenticated-route-mixin";
import ScrollToTopMixin from "../mixins/scroll-top";
import PollingRoute from "../mixins/polling-route";

export default Route.extend(
    AuthenticatedRouteMixin,
    ScrollToTopMixin,
    PollingRoute,
    {
        offline: service(),
        api: service(),
        title: "Session Tests",
        favicon: service(),

        model({ id }) {
            let self = this;
            return self.store.query("session", {id: id}).then(function(sessions) {
                let session = sessions.get('firstObject');

                if (!session) {
                    return reject({not_found: true});
                }

                return hash({
                    session_model: session,
                    user: self.store.find("user", session.get("user_id")),

                    timings: self.get('api').call('get_timings', {session_id: parseInt(session.id)}).then(function(timings) {
                        let returned = [];
                        for (let name in timings.result) {
                            returned.push({name: name, total: timings.result[name]});
                        }
                        return returned;
                    }),
                    metadata: self.get("api")
                        .call("get_metadata", {
                            entity_type: "session",
                            entity_id: parseInt(session.id)
                        })
                        .then(
                            function(r)
                            {
                                if (session.data.child_id != null) {
                                    delete r.result['slash::commandline'];
                                }
                                return r.result;
                            }
                        ),
                });
            });
        },

        afterModel(model) {
            let session = model.session_model;
            this.get('favicon').set_by_session(session);
        },

        deactivate() {
            this.get('favicon').reset();
        },

        should_auto_refresh: function() {
            const end_time = this.modelFor("session").session_model.get("end_time");
            return end_time === null;
        },

        setupController: function(controller, model) {
            this._super(controller, model);
            controller.setProperties(model);
            this.get("offline");
        },

        resetController(controller) {
            controller.set("current_test", null);
        }
    }
);
