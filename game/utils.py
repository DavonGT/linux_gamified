"""Utility functions for game session management."""
from typing import Optional
from .constants import (
    DEFAULT_LIVES,
    DEFAULT_TIME,
    DEFAULT_SCORE,
    SURVIVAL_MODE,
    TIME_ATTACK_MODE,
    HARDCORE_SURVIVAL_MODE,
    HARDCORE_TIME_ATTACK_MODE,
    GAME_MODES,
)

def initialize_game_session(session: dict, mode: str) -> None:
    """Initialize the game session with default values based on game mode.
    
    Args:
        session: The session dictionary to initialize
        mode: The game mode to set up
    """
    if mode not in GAME_MODES:
        raise ValueError(f"Invalid game mode: {mode}")
    
    session['mode'] = mode
    session['score'] = DEFAULT_SCORE
    
    if SURVIVAL_MODE in mode or HARDCORE_SURVIVAL_MODE in mode:
        session['lives'] = DEFAULT_LIVES
        session['time'] = None
    elif TIME_ATTACK_MODE in mode or HARDCORE_TIME_ATTACK_MODE in mode:
        session['lives'] = None
        session['time'] = DEFAULT_TIME

def clear_game_session(session: dict) -> None:
    """Clear all game-related data from the session.
    
    Args:
        session: The session dictionary to clear
    """
    session['score'] = DEFAULT_SCORE
    session['lives'] = DEFAULT_LIVES
    session.pop('mode', None)
    session.pop('time', None)

def get_session_score(session: dict) -> int:
    """Get the current score from the session.
    
    Args:
        session: The session dictionary
    
    Returns:
        The current score
    """
    return session.get('score', DEFAULT_SCORE)

def get_session_lives(session: dict) -> Optional[int]:
    """Get the current lives from the session.
    
    Args:
        session: The session dictionary
    
    Returns:
        The current number of lives or None if not applicable
    """
    return session.get('lives')

def get_session_time(session: dict) -> Optional[int]:
    """Get the current time from the session.
    
    Args:
        session: The session dictionary
    
    Returns:
        The current time or None if not applicable
    """
    return session.get('time')

def update_session_score(session: dict, points: int) -> None:
    """Update the score in the session.
    
    Args:
        session: The session dictionary
        points: Points to add to the score
    """
    session['score'] = session.get('score', DEFAULT_SCORE) + points

def decrement_session_lives(session: dict) -> Optional[int]:
    """Decrement the lives in the session.
    
    Args:
        session: The session dictionary
    
    Returns:
        The new number of lives or None if not applicable
    """
    if 'lives' in session and session['lives'] is not None:
        session['lives'] -= 1
        return session['lives']
    return None
