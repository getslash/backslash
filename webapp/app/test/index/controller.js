import Ember from 'ember';


export default Ember.Controller.extend({

    is_method: Ember.computed.notEmpty('info.class_name'),

    test_details: function() {
        let self = this;
        let test = self.get('test');

        let returned = Ember.Object.create({
            'File name': test.get('info.file_name'),

        });

        returned.set(self.get('is_method')?'Method':'Function', test.get('info.name'));

        if (self.get('test.is_skipped')) {
            returned.set('Skip Reason', self.get('test.skip_reason'));
        }

        return returned;

    }.property('test'),


    scm_details: function() {
        let self = this;
        let test = self.get('test');

        if (!test.get('scm')) {
            return {};
        }

        return Ember.Object.create({
            'Revision': test.get('scm_revision'),
            'File Hash': test.get('file_hash')
        });

    }.property('test'),

    test: Ember.computed.oneWay('parent_controller.test'),
});
