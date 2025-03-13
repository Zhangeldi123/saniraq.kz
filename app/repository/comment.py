from sqlalchemy.orm import Session
from models.comment import Comments
from fastapi import HTTPException, status

class CommentsRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_comment(self, house_id: int, user_id: int, text: str):
        comment = Comments(house_id=house_id, user_id=user_id, text=text)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments(self, house_id: int):
        return self.db.query(Comments).filter(Comments.house_id == house_id).all()

    def update_comment(self, house_id: int, comment_id: int, user_id: int, text: str):
        comment = self.db.query(Comments).filter(Comments.id == comment_id, Comments.house_id == house_id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
        
        comment.text = text
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete_comment(self, house_id: int, comment_id: int, user_id: int):
        comment = self.db.query(Comments).filter(Comments.id == comment_id, Comments.house_id == house_id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
        
        self.db.delete(comment)
        self.db.commit()
        return {"detail": "Comment deleted successfully"}
