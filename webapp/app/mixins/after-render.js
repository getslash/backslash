import Ember from 'ember';

export default Ember.Mixin.create({

  /*
   This hook is guaranteed to be executed when the root element of this view has been inserted into the DOM.
   */
  didInsertElement : function(){
    this._super();
    Ember.run.scheduleOnce('afterRender', this, this.afterRenderEvent);
  },

  afterRenderEvent : Ember.K
});
