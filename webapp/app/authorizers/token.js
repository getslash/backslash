import Base from 'simple-auth/authorizers/base';

export default Base.extend({
  authorize: function(jqXHR, requestOptions) {
    var session = this.get('session');
    if (!session.isAuthenticated) {
      return;
    }

    var auth_token = session.content.auth_token;
    if (requestOptions.headers === undefined) {
      requestOptions.headers = {};
    }

    requestOptions.headers['Authentication-Token'] = auth_token;
  }
});
