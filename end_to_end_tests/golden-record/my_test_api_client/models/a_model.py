import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.an_enum import AnEnum
from ..models.different_enum import DifferentEnum
from ..models.free_form_model import FreeFormModel
from ..models.model_with_union_property import ModelWithUnionProperty
from ..types import UNSET, Unset

T = TypeVar("T", bound="AModel")


@attr.s(auto_attribs=True)
class AModel:
    """ A Model for testing all the ways custom objects can be used  """

    an_enum_value: AnEnum
    a_camel_date_time: Union[datetime.datetime, datetime.date]
    a_date: datetime.date
    required_not_nullable: str
    model: ModelWithUnionProperty
    one_of_models: Union[FreeFormModel, ModelWithUnionProperty]
    a_nullable_date: Optional[datetime.date]
    required_nullable: Optional[str]
    nullable_model: Optional[ModelWithUnionProperty]
    nullable_one_of_models: Union[None, FreeFormModel, ModelWithUnionProperty]
    nested_list_of_enums: Union[Unset, List[List[DifferentEnum]]] = UNSET
    attr_1_leading_digit: Union[Unset, str] = UNSET
    not_required_nullable: Union[Unset, None, str] = UNSET
    not_required_not_nullable: Union[Unset, str] = UNSET
    not_required_model: Union[Unset, ModelWithUnionProperty] = UNSET
    not_required_nullable_model: Union[Unset, None, ModelWithUnionProperty] = UNSET
    not_required_one_of_models: Union[Unset, FreeFormModel, ModelWithUnionProperty] = UNSET
    not_required_nullable_one_of_models: Union[Unset, None, FreeFormModel, ModelWithUnionProperty, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        an_enum_value = self.an_enum_value.value

        if isinstance(self.a_camel_date_time, datetime.datetime):
            a_camel_date_time = self.a_camel_date_time.isoformat()

        else:
            a_camel_date_time = self.a_camel_date_time.isoformat()

        a_date = self.a_date.isoformat()
        required_not_nullable = self.required_not_nullable
        model = self.model.to_dict()

        if isinstance(self.one_of_models, FreeFormModel):
            one_of_models = self.one_of_models.to_dict()

        else:
            one_of_models = self.one_of_models.to_dict()

        nested_list_of_enums: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.nested_list_of_enums, Unset):
            nested_list_of_enums = []
            for nested_list_of_enums_item_data in self.nested_list_of_enums:
                nested_list_of_enums_item = []
                for nested_list_of_enums_item_item_data in nested_list_of_enums_item_data:
                    nested_list_of_enums_item_item = nested_list_of_enums_item_item_data.value

                    nested_list_of_enums_item.append(nested_list_of_enums_item_item)

                nested_list_of_enums.append(nested_list_of_enums_item)

        a_nullable_date = self.a_nullable_date.isoformat() if self.a_nullable_date else None
        attr_1_leading_digit = self.attr_1_leading_digit
        required_nullable = self.required_nullable
        not_required_nullable = self.not_required_nullable
        not_required_not_nullable = self.not_required_not_nullable
        nullable_model = self.nullable_model.to_dict() if self.nullable_model else None

        not_required_model: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.not_required_model, Unset):
            not_required_model = self.not_required_model.to_dict()

        not_required_nullable_model: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.not_required_nullable_model, Unset):
            not_required_nullable_model = (
                self.not_required_nullable_model.to_dict() if self.not_required_nullable_model else None
            )

        nullable_one_of_models: Union[None, Dict[str, Any]]
        if isinstance(self.nullable_one_of_models, Unset):
            nullable_one_of_models = UNSET
        if self.nullable_one_of_models is None:
            nullable_one_of_models = None
        elif isinstance(self.nullable_one_of_models, FreeFormModel):
            nullable_one_of_models = self.nullable_one_of_models.to_dict()

        else:
            nullable_one_of_models = self.nullable_one_of_models.to_dict()

        not_required_one_of_models: Union[Unset, Dict[str, Any]]
        if isinstance(self.not_required_one_of_models, Unset):
            not_required_one_of_models = UNSET
        elif isinstance(self.not_required_one_of_models, FreeFormModel):
            not_required_one_of_models = UNSET
            if not isinstance(self.not_required_one_of_models, Unset):
                not_required_one_of_models = self.not_required_one_of_models.to_dict()

        else:
            not_required_one_of_models = UNSET
            if not isinstance(self.not_required_one_of_models, Unset):
                not_required_one_of_models = self.not_required_one_of_models.to_dict()

        not_required_nullable_one_of_models: Union[Unset, None, Dict[str, Any], str]
        if isinstance(self.not_required_nullable_one_of_models, Unset):
            not_required_nullable_one_of_models = UNSET
        elif self.not_required_nullable_one_of_models is None:
            not_required_nullable_one_of_models = None
        elif isinstance(self.not_required_nullable_one_of_models, FreeFormModel):
            not_required_nullable_one_of_models = UNSET
            if not isinstance(self.not_required_nullable_one_of_models, Unset):
                not_required_nullable_one_of_models = self.not_required_nullable_one_of_models.to_dict()

        elif isinstance(self.not_required_nullable_one_of_models, ModelWithUnionProperty):
            not_required_nullable_one_of_models = UNSET
            if not isinstance(self.not_required_nullable_one_of_models, Unset):
                not_required_nullable_one_of_models = self.not_required_nullable_one_of_models.to_dict()

        else:
            not_required_nullable_one_of_models = self.not_required_nullable_one_of_models

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "an_enum_value": an_enum_value,
                "aCamelDateTime": a_camel_date_time,
                "a_date": a_date,
                "required_not_nullable": required_not_nullable,
                "model": model,
                "one_of_models": one_of_models,
                "a_nullable_date": a_nullable_date,
                "required_nullable": required_nullable,
                "nullable_model": nullable_model,
                "nullable_one_of_models": nullable_one_of_models,
            }
        )
        if nested_list_of_enums is not UNSET:
            field_dict["nested_list_of_enums"] = nested_list_of_enums
        if attr_1_leading_digit is not UNSET:
            field_dict["1_leading_digit"] = attr_1_leading_digit
        if not_required_nullable is not UNSET:
            field_dict["not_required_nullable"] = not_required_nullable
        if not_required_not_nullable is not UNSET:
            field_dict["not_required_not_nullable"] = not_required_not_nullable
        if not_required_model is not UNSET:
            field_dict["not_required_model"] = not_required_model
        if not_required_nullable_model is not UNSET:
            field_dict["not_required_nullable_model"] = not_required_nullable_model
        if not_required_one_of_models is not UNSET:
            field_dict["not_required_one_of_models"] = not_required_one_of_models
        if not_required_nullable_one_of_models is not UNSET:
            field_dict["not_required_nullable_one_of_models"] = not_required_nullable_one_of_models

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        an_enum_value = AnEnum(d.pop("an_enum_value"))

        def _parse_a_camel_date_time(data: Union[str]) -> Union[datetime.datetime, datetime.date]:
            a_camel_date_time: Union[datetime.datetime, datetime.date]
            try:
                if not isinstance(data, str):
                    raise TypeError()
                a_camel_date_time = isoparse(data)

                return a_camel_date_time
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            a_camel_date_time = isoparse(data).date()

            return a_camel_date_time

        a_camel_date_time = _parse_a_camel_date_time(d.pop("aCamelDateTime"))

        a_date = isoparse(d.pop("a_date")).date()

        required_not_nullable = d.pop("required_not_nullable")

        model = ModelWithUnionProperty.from_dict(d.pop("model"))

        def _parse_one_of_models(data: Union[Dict[str, Any]]) -> Union[FreeFormModel, ModelWithUnionProperty]:
            one_of_models: Union[FreeFormModel, ModelWithUnionProperty]
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                one_of_models = FreeFormModel.from_dict(data)

                return one_of_models
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            one_of_models = ModelWithUnionProperty.from_dict(data)

            return one_of_models

        one_of_models = _parse_one_of_models(d.pop("one_of_models"))

        nested_list_of_enums = []
        _nested_list_of_enums = d.pop("nested_list_of_enums", UNSET)
        for nested_list_of_enums_item_data in _nested_list_of_enums or []:
            nested_list_of_enums_item = []
            _nested_list_of_enums_item = nested_list_of_enums_item_data
            for nested_list_of_enums_item_item_data in _nested_list_of_enums_item:
                nested_list_of_enums_item_item = DifferentEnum(nested_list_of_enums_item_item_data)

                nested_list_of_enums_item.append(nested_list_of_enums_item_item)

            nested_list_of_enums.append(nested_list_of_enums_item)

        a_nullable_date = None
        _a_nullable_date = d.pop("a_nullable_date")
        if _a_nullable_date is not None:
            a_nullable_date = isoparse(cast(str, _a_nullable_date)).date()

        attr_1_leading_digit = d.pop("1_leading_digit", UNSET)

        required_nullable = d.pop("required_nullable")

        not_required_nullable = d.pop("not_required_nullable", UNSET)

        not_required_not_nullable = d.pop("not_required_not_nullable", UNSET)

        nullable_model = None
        _nullable_model = d.pop("nullable_model")
        if _nullable_model is not None:
            nullable_model = ModelWithUnionProperty.from_dict(_nullable_model)

        not_required_model: Union[Unset, ModelWithUnionProperty] = UNSET
        _not_required_model = d.pop("not_required_model", UNSET)
        if not isinstance(_not_required_model, Unset):
            not_required_model = ModelWithUnionProperty.from_dict(_not_required_model)

        not_required_nullable_model = None
        _not_required_nullable_model = d.pop("not_required_nullable_model", UNSET)
        if _not_required_nullable_model is not None and not isinstance(_not_required_nullable_model, Unset):
            not_required_nullable_model = ModelWithUnionProperty.from_dict(_not_required_nullable_model)

        def _parse_nullable_one_of_models(
            data: Union[None, Dict[str, Any]]
        ) -> Union[None, FreeFormModel, ModelWithUnionProperty]:
            nullable_one_of_models: Union[None, FreeFormModel, ModelWithUnionProperty]
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                nullable_one_of_models = FreeFormModel.from_dict(data)

                return nullable_one_of_models
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            nullable_one_of_models = ModelWithUnionProperty.from_dict(data)

            return nullable_one_of_models

        nullable_one_of_models = _parse_nullable_one_of_models(d.pop("nullable_one_of_models"))

        def _parse_not_required_one_of_models(
            data: Union[Unset, Dict[str, Any]]
        ) -> Union[Unset, FreeFormModel, ModelWithUnionProperty]:
            not_required_one_of_models: Union[Unset, FreeFormModel, ModelWithUnionProperty]
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_required_one_of_models = UNSET
                _not_required_one_of_models = data
                if not isinstance(_not_required_one_of_models, Unset):
                    not_required_one_of_models = FreeFormModel.from_dict(_not_required_one_of_models)

                return not_required_one_of_models
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            not_required_one_of_models = UNSET
            _not_required_one_of_models = data
            if not isinstance(_not_required_one_of_models, Unset):
                not_required_one_of_models = ModelWithUnionProperty.from_dict(_not_required_one_of_models)

            return not_required_one_of_models

        not_required_one_of_models = _parse_not_required_one_of_models(d.pop("not_required_one_of_models", UNSET))

        def _parse_not_required_nullable_one_of_models(
            data: Union[Unset, None, Dict[str, Any], str]
        ) -> Union[Unset, None, FreeFormModel, ModelWithUnionProperty, str]:
            not_required_nullable_one_of_models: Union[Unset, None, FreeFormModel, ModelWithUnionProperty, str]
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_required_nullable_one_of_models = UNSET
                _not_required_nullable_one_of_models = data
                if not isinstance(_not_required_nullable_one_of_models, Unset):
                    not_required_nullable_one_of_models = FreeFormModel.from_dict(_not_required_nullable_one_of_models)

                return not_required_nullable_one_of_models
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                not_required_nullable_one_of_models = UNSET
                _not_required_nullable_one_of_models = data
                if not isinstance(_not_required_nullable_one_of_models, Unset):
                    not_required_nullable_one_of_models = ModelWithUnionProperty.from_dict(
                        _not_required_nullable_one_of_models
                    )

                return not_required_nullable_one_of_models
            except:  # noqa: E722
                pass
            return cast(Union[Unset, None, FreeFormModel, ModelWithUnionProperty, str], data)

        not_required_nullable_one_of_models = _parse_not_required_nullable_one_of_models(
            d.pop("not_required_nullable_one_of_models", UNSET)
        )

        a_model = cls(
            an_enum_value=an_enum_value,
            a_camel_date_time=a_camel_date_time,
            a_date=a_date,
            required_not_nullable=required_not_nullable,
            model=model,
            one_of_models=one_of_models,
            nested_list_of_enums=nested_list_of_enums,
            a_nullable_date=a_nullable_date,
            attr_1_leading_digit=attr_1_leading_digit,
            required_nullable=required_nullable,
            not_required_nullable=not_required_nullable,
            not_required_not_nullable=not_required_not_nullable,
            nullable_model=nullable_model,
            not_required_model=not_required_model,
            not_required_nullable_model=not_required_nullable_model,
            nullable_one_of_models=nullable_one_of_models,
            not_required_one_of_models=not_required_one_of_models,
            not_required_nullable_one_of_models=not_required_nullable_one_of_models,
        )

        return a_model
