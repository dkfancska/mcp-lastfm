"""Pydantic input models and enums for Last.fm MCP tools."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

DEFAULT_LIMIT = 20


class Period(str, Enum):
    """Time period for top charts."""
    OVERALL = "overall"
    WEEK = "7day"
    MONTH = "1month"
    THREE_MONTHS = "3month"
    SIX_MONTHS = "6month"
    YEAR = "12month"


class UserInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(..., description="Last.fm username", min_length=1, max_length=64)


class UserTopInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(..., description="Last.fm username", min_length=1, max_length=64)
    period: Period = Field(
        default=Period.OVERALL,
        description="Time period: overall, 7day, 1month, 3month, 6month, 12month",
    )
    limit: int = Field(default=DEFAULT_LIMIT, description="Number of results (1-50)", ge=1, le=50)
    page: int = Field(default=1, description="Page number for pagination", ge=1)


class RecentTracksInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    username: str = Field(..., description="Last.fm username", min_length=1, max_length=64)
    limit: int = Field(default=DEFAULT_LIMIT, description="Number of results (1-50)", ge=1, le=50)
    page: int = Field(default=1, description="Page number for pagination", ge=1)


class SearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    query: str = Field(..., description="Search query", min_length=1, max_length=200)
    limit: int = Field(default=DEFAULT_LIMIT, description="Number of results (1-30)", ge=1, le=30)
    page: int = Field(default=1, description="Page number for pagination", ge=1)

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class ArtistInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    artist: str = Field(..., description="Artist name", min_length=1, max_length=200)


class AlbumInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    artist: str = Field(..., description="Artist name", min_length=1, max_length=200)
    album: str = Field(..., description="Album name", min_length=1, max_length=200)


class TrackInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    artist: str = Field(..., description="Artist name", min_length=1, max_length=200)
    track: str = Field(..., description="Track name", min_length=1, max_length=200)


class SimilarInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    artist: str = Field(..., description="Artist name", min_length=1, max_length=200)
    limit: int = Field(default=DEFAULT_LIMIT, description="Number of results (1-50)", ge=1, le=50)


class ArtistTopInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    artist: str = Field(..., description="Artist name", min_length=1, max_length=200)
    limit: int = Field(default=DEFAULT_LIMIT, description="Number of results (1-50)", ge=1, le=50)
    page: int = Field(default=1, description="Page number for pagination", ge=1)
