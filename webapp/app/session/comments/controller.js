import CommentsController from '../../controllers/comments_controller';

export default CommentsController.extend({


    getSaveCommentParams: function(comment) {
        return {
            comment: comment.get('comment'),
            session_id: parseInt(this.get('session.id'))
        };
    }

});
