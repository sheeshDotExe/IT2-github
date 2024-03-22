from pydantic import BaseModel, Field


class MediaElement(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias="Year")
    imdb_id: str = Field(alias="imdbID")
    media_type: str = Field(alias="Type")
    poster_url: str = Field(alias="Poster")


class MediaElementDetailed(BaseModel):
    plot: str = Field(alias="Plot")
    actors: str = Field(alias="Actors")
    director: str = Field(alias="Director")
    genre: str = Field(alias="Genre")
    rated: str = Field(alias="Rated")
    imdb_rating: str = Field(alias="imdbRating")
    language: str = Field(alias="Language")
    country: str = Field(alias="Country")
    awards: str = Field(alias="Awards")


class MovieElement(MediaElementDetailed):
    runtime: str = Field(alias="Runtime")
    dvd_release: str = Field(alias="DVD")
    box_office: str = Field(alias="BoxOffice")


class SeriesElement(MediaElementDetailed):
    total_seasons: str = Field(alias="totalSeasons")


class GameElement(MediaElementDetailed):
    pass
