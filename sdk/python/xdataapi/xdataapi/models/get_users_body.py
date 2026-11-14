from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetUsersBody")


@_attrs_define
class GetUsersBody:
    """Exactly one of `handles` and `ids`.

    Attributes:
        handles (list[str] | Unset):  Example: ['x', 'github', 'vercel'].
        ids (list[str] | Unset):  Example: ['783214', '13334762'].
    """

    handles: list[str] | Unset = UNSET
    ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        handles: list[str] | Unset = UNSET
        if not isinstance(self.handles, Unset):
            handles = self.handles

        ids: list[str] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if handles is not UNSET:
            field_dict["handles"] = handles
        if ids is not UNSET:
            field_dict["ids"] = ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        handles = cast(list[str], d.pop("handles", UNSET))

        ids = cast(list[str], d.pop("ids", UNSET))

        get_users_body = cls(
            handles=handles,
            ids=ids,
        )

        get_users_body.additional_properties = d
        return get_users_body

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
