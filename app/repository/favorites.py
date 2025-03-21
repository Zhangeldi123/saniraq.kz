from sqlalchemy.orm import Session
from ..models.favorites import Favorites
from ..models.house import Houses
from fastapi import HTTPException, status


class FavoritesRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_favorite(self, user_id: int, house_id: int):
        """Добавляет объявление (house) в избранное"""
        # Проверяем, существует ли дом
        house = self.db.query(Houses).filter(Houses.id == house_id).first()
        if not house:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="House not found")

        # Проверяем, нет ли уже этого дома в избранном
        existing_favorite = (
            self.db.query(Favorites)
            .filter(Favorites.user_id == user_id, Favorites.house_id == house_id)
            .first()
        )
        if existing_favorite:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already in favorites")

        # Добавляем в избранное
        new_favorite = Favorites(user_id=user_id, house_id=house_id)
        self.db.add(new_favorite)
        self.db.commit()
        self.db.refresh(new_favorite)
        return {"message": "Added to favorites"}

    def get_favorites(self, user_id: int):
        """Получает список избранных домов пользователя"""
        favorites = (
            self.db.query(Favorites)
            .filter(Favorites.user_id == user_id)
            .join(Houses, Favorites.house_id == Houses.id)
            .all()
        )

        return {
            "houses": [
                {"_id": f.house.id, "address": f.house.address}
                for f in favorites
            ]
        }

    def delete_favorite(self, user_id: int, house_id: int):
        """Удаляет дом из избранного"""
        favorite = (
            self.db.query(Favorites)
            .filter(Favorites.user_id == user_id, Favorites.house_id == house_id)
            .first()
        )
        if not favorite:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

        self.db.delete(favorite)
        self.db.commit()
        return {"message": "Removed from favorites"}
