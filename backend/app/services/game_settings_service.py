from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.repositories.game_settings_repository import GameSettingsRepository


class GameSettingsService:

    @staticmethod
    def get_settings(db: Session):
        """ Retrieves global game configuration. """
        settings = GameSettingsRepository.get_settings(db)

        if not settings:
            raise HTTPException(status_code=404, detail="Game settings not found")

        return settings

    @staticmethod
    def update_settings(db: Session, payload):
        """ Updates visibility of global, chapter and challenge leaderboards. """
        settings = GameSettingsRepository.update_settings(
            db,
            payload.show_global_leaderboard,
            payload.show_chapter_leaderboard,
            payload.show_challenge_leaderboard
        )
        return settings
