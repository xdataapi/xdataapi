from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_body_code import ErrorBodyCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorBody")


@_attrs_define
class ErrorBody:
    """The failure itself. `code` is stable; match on it, never on `message`.

    Attributes:
        code (ErrorBodyCode):
        message (str):
        top_up_url (str | Unset): Only on `no_credits`. The page where a pack is bought. Example:
            https://xdataapi.io/dashboard/billing.
    """

    code: ErrorBodyCode
    message: str
    top_up_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        message = self.message

        top_up_url = self.top_up_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if top_up_url is not UNSET:
            field_dict["top_up_url"] = top_up_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = ErrorBodyCode(d.pop("code"))

        message = d.pop("message")

        top_up_url = d.pop("top_up_url", UNSET)

        error_body = cls(
            code=code,
            message=message,
            top_up_url=top_up_url,
        )

        error_body.additional_properties = d
        return error_body

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
