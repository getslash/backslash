import SessionsRoute from "../../sessions/route";
export default SessionsRoute.extend({
  needs: ["user"],

  get_user_id_parameter: function() {
    return this.modelFor("user").id;
  },

  renderTemplate() {
    this.render("sessions", {
      controller: "user.sessions"
    });
  }
});
