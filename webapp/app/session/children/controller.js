import { sort } from '@ember/object/computed';
import Controller from '@ember/controller';


export default Controller.extend({
    sortProperties: ['child_id:asc'],
    sortedModel: sort('children', 'sortProperties'),
});
