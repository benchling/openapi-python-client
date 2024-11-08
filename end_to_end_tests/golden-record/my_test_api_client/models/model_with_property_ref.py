from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_name import ModelName


T = TypeVar("T", bound="ModelWithPropertyRef")


@_attrs_define
class ModelWithPropertyRef:
    """
    Attributes:
        inner (Union[Unset, ModelName]):
    """

    inner: Union[Unset, "ModelName"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prop1: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.inner, Unset):
            prop1 = self.inner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict = {
            **field_dict,
            **({} if prop1 is UNSET else {"inner": prop1}),
        }

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_name import ModelName

        d = src_dict.copy()
        _inner = d.pop("inner", UNSET)
        inner: Union[Unset, ModelName]
        if isinstance(_inner, Unset):
            inner = UNSET
        else:
            inner = ModelName.from_dict(_inner)

        model_with_property_ref = cls(
            inner=inner,
        )

        model_with_property_ref.additional_properties = d
        return model_with_property_ref

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
