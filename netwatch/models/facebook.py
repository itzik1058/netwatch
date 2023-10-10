from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from netwatch.core.database import Base


class FacebookPost(Base):
    __tablename__ = "facebook_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_name: Mapped[str]
    post_id: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str]
    content: Mapped[str]
    comments: Mapped[list["FacebookComment"]] = relationship(back_populates="post")


class FacebookComment(Base):
    __tablename__ = "facebook_comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey(
            "facebook_post.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    comment_id: Mapped[str | None]
    content: Mapped[str] = mapped_column(unique=True)
    post: Mapped[FacebookPost] = relationship(back_populates="comments")
