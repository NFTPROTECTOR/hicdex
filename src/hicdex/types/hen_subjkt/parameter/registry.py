# generated by datamodel-codegen:
#   filename:  registry.json

from __future__ import annotations

from pydantic import BaseModel


class RegistryParameter(BaseModel):
    metadata: str
    subjkt: str
