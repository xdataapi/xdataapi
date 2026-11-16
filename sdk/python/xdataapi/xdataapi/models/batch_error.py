from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_error_code import BatchErrorCode
from ..models.not_found_reason import NotFoundReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchError")


@_attrs_define
class BatchError:
    """
    Attributes:
        input_ (str): The handle or id as sent.
        code (BatchErrorCode):
        message (str):
        reason (NotFoundReason | Unset): Only on a profile `not_found`, and only when X says why the account is not
            there: `suspended`,
            `age_restricted` (X shows the account only to a logged-in session, and did not show it to ours), or
            `unavailable` for any other reason X names. Absent for an account that was deleted or never existed:
            X does not tell those two apart. A protected account is not a `not_found`: its profile comes back with
            `protected: true`.
    """

    input_: str
    code: BatchErrorCode
    message: str
    reason: NotFoundReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        code = self.code.value

        message = self.message

        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "code": code,
                "message": message,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_ = d.pop("input")

        code = BatchErrorCode(d.pop("code"))

        message = d.pop("message")

        _reason = d.pop("reason", UNSET)
        reason: NotFoundReason | Unset
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = NotFoundReason(_reason)

        batch_error = cls(
            input_=input_,
            code=code,
            message=message,
            reason=reason,
        )

        batch_error.additional_properties = d
        return batch_error

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
