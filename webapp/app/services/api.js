import $ from 'jquery';
import Service from '@ember/service';

export default Service.extend({
  call: function(name, params = {}) {
    return $.ajax({
      type: "POST",
      url: "/api/" + name,
      contentType: "application/json",
      data: JSON.stringify(params)
    });
  }
});
