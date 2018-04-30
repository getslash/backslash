import Component from '@ember/component';
import { inject as service } from '@ember/service';

export default Component.extend({
  classNames: ["input-group"],
  display: service(),
   actions: {
     toggleModal: function() {
       this.get("display").toggleProperty('show_help');
     }
   }
});
