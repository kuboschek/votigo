

from abc import abstractmethod
from typing import Iterable, Literal, Union

from jsonpointer import JsonPointer, JsonPointerException
from pydantic import BaseModel, Field, field_validator

BasicValue = str | int | bool | float
BasicDict = dict[str, BasicValue | Iterable[BasicValue] | 'BasicDict']

class AndCondition(BaseModel):
    type: Literal["AND"] = "AND"
    parts: list['ConditionTree'] = Field(discriminator="type")

    def test(self, user_attributes: dict):
        return all(part.test(user_attributes) for part in self.parts)

class OrCondition(BaseModel):
    type: Literal["OR"] = "OR"
    parts: list['ConditionTree'] = Field(discriminator="type")

    def test(self, user_attributes: dict):
        return any(part.test(user_attributes) for part in self.parts)

class EqCondition(BaseModel):
    type: Literal["EQ"] = "EQ"
    pointer: str
    """ JSON Pointer to the value in the user attributes to compare against"""

    target_value: BasicValue

    @field_validator("pointer")
    @classmethod
    def validate_pointer(cls, value):
        try:
            JsonPointer(value)
        except JsonPointerException as e:
            raise ValueError(str(e))
        
        return value
    
    def test(self, user_attributes: BasicDict):
        pointer_inst = JsonPointer(self.pointer)

        return pointer_inst.get(user_attributes) == self.target_value
    

ConditionTree = Union[AndCondition, OrCondition, EqCondition]

class Condition(BaseModel):
    tree: ConditionTree = Field(discriminator="type")

    def test(self, user_attributes: BasicDict):
        try:
            return self.tree.test(user_attributes)
        except JsonPointerException:
            return False # Fail safe