import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class VehicleHornIDs(TypedDict):
    """Structure of loot/vehicle_horn_ids.csv"""

    id: int
    ref: str
    rarity: int  # Not defined in luashared/csvutils.lua
    price: int  # Not defined in luashared/csvutils.lua
    salvage: int  # Not defined in luashared/csvutils.lua
    license: int  # Not defined in luashared/csvutils.lua
    premium: int  # bool, not defined in luashared/csvutils.lua


class VehicleHornsTable(TypedDict):
    """Structure of mp_cp/vehiclehorns.csv"""

    index: int
    ref: str
    name: str
    mtxAlias: str
    apcAlias: str
    apcAliasUI: str
    atvAlias: str
    atvAliasUI: str
    cargoAlias: str
    cargoAliasUI: str
    jeepAlias: str
    jeepAliasUI: str
    littleBirdAlias: str
    littleBirdAliasUI: str
    tacRoverAlias: str
    tacRoverAliasUI: str
    motorcycleAlias: str
    motorcycleAliasUI: str
    lootImage: str
    hideInUI: int  # bool
    unlockText: str


class VehicleHorns:
    """Vehicle Horn XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Vehicle Horn XAssets."""

        horns: List[Dict[str, Any]] = []

        horns = VehicleHorns.IDs(self, horns)
        horns = VehicleHorns.Table(self, horns)

        Utility.WriteFile(self, f"{self.eXAssets}/vehicleHorns.json", horns)

        log.info(f"Compiled {len(horns):,} Vehicle Horns")

    def IDs(self: Any, horns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/vehicle_horn_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/vehicle_horn_ids.csv", VehicleHornIDs
        )

        if ids is None:
            return horns

        for entry in ids:
            horns.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "flavor": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "available": self.ModernWarfare.GetTitleAvailability(
                        entry.get("id")
                    ),
                    "unlock": None,
                    "hidden": None,
                    "image": "ui_vehicle_horn",
                    "background": "ui_loot_bg_vehicle_horn",
                }
            )

        return horns

    def Table(self: Any, horns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp_cp/vehiclehorns.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp_cp/vehiclehorns.csv", VehicleHornsTable
        )

        if table is None:
            return horns

        for horn in horns:
            for entry in table:
                if horn.get("altId") != entry.get("ref"):
                    continue

                horn["name"] = self.localize.get(entry.get("name"))
                horn["flavor"] = self.localize.get(entry.get("flavorText"))
                horn["unlock"] = self.localize.get(entry.get("unlockText")).replace(
                    "&&1 ", ""
                )
                horn["hidden"] = bool(entry.get("hideInUI"))

        return horns
