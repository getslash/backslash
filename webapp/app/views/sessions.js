import Ember from 'ember';
import AfterRender from '../mixins/after-render';

export default Ember.View.extend(AfterRender, {
  afterRenderEvent: function() {
    this.get('controller').send("sortBy", '');   //just to refresh the up/down triangle
  }

});
