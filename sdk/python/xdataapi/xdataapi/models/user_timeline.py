from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tweet import Tweet


T = TypeVar("T", bound="UserTimeline")


@_attrs_define
class UserTimeline:
    """
    Attributes:
        user_id (str): The user id from the request.
        tweets (list[Tweet]): Newest first. Empty when the user has no public tweets.
        next_cursor (str | Unset): Send it to `/v1/users/{user}/tweets` as `cursor` to read on. Not there on the last
            page.
    """

    user_id: str
    tweets: list[Tweet]
    next_cursor: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        tweets = []
        for tweets_item_data in self.tweets:
            tweets_item = tweets_item_data.to_dict()
            tweets.append(tweets_item)

        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "tweets": tweets,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tweet import Tweet  # noqa: PLC0415

        d = dict(src_dict)
        user_id = d.pop("user_id")

        tweets = []
        _tweets = d.pop("tweets")
        for tweets_item_data in _tweets:
            tweets_item = Tweet.from_dict(tweets_item_data)

            tweets.append(tweets_item)

        next_cursor = d.pop("next_cursor", UNSET)

        user_timeline = cls(
            user_id=user_id,
            tweets=tweets,
            next_cursor=next_cursor,
        )

        user_timeline.additional_properties = d
        return user_timeline

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
