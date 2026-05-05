from fastapi import HTTPException
from typing import cast
from sqlalchemy.orm import Session
from app.models.game_settings import GameSettings


class GameSettingsRepository:

    @staticmethod
    def get_settings(db: Session) -> GameSettings:
        # Obtains game configuration
        settings = db.query(GameSettings).first()

        if not settings:
            raise HTTPException(
                status_code=500,
                detail="Game settings not initialized"
            )

        return cast(GameSettings, settings)

    @staticmethod
    def update_settings(
            db: Session,
            show_global: bool | None,
            show_chapter: bool | None,
            show_challenge: bool | None
    ) -> GameSettings:
        # Updates game configuration
        settings = GameSettingsRepository.get_settings(db)

        if show_global is not None:
            settings.show_global_leaderboard = show_global

        if show_chapter is not None:
            settings.show_chapter_leaderboard = show_chapter

        if show_challenge is not None:
            settings.show_challenge_leaderboard = show_challenge

        db.commit()
        db.refresh(settings)
        return settings
