import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class DLCIDs(TypedDict):
    """Structure of loot/dlc_ids.csv"""

    id: int
    name: str
    type: str
    CPAmount: int
    PS4ID: str
    XB1ID: str
    battleNetID: int
    wegameID: int
    title: str
    image: str
    isCODPoints: int  # bool
    shouldShowPopup: int  # bool
    item1: int  # itemStart in luashared/csvutils.lua
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    item7: int
    item8: int
    item9: int
    item10: int
    item11: int
    item12: int
    item13: int
    item14: int
    item15: int
    item16: int
    item17: int
    item18: int
    item19: int
    item20: int  # itemEnd in luashared/csvutils.lua
    item21: int
    item22: int
    item23: int
    item24: int
    item25: int
    item26: int
    item27: int
    item28: int
    item29: int
    item30: int
    item31: int
    item32: int
    item33: int
    item34: int
    item35: int
    item36: int
    item37: int
    item38: int
    item39: int
    item40: int
    item41: int
    item42: int
    item43: int
    item44: int
    item45: int
    item46: int
    item47: int
    item48: int
    item49: int
    item50: int
    item51: int
    item52: int
    item53: int
    item54: int
    item55: int
    item56: int
    item57: int
    item58: int
    item59: int
    item60: int
    item61: int
    item62: int
    item63: int
    item64: int
    item65: int
    item66: int
    item67: int
    item68: int
    item69: int
    item70: int
    item71: int
    item72: int
    item73: int
    item74: int
    item75: int
    item76: int
    item77: int
    item78: int
    item79: int
    item80: int
    item81: int
    item82: int
    item83: int


class DLC:
    """DLC XAssets."""

    def Compile(self: Any) -> None:
        """Compile the DLC XAssets."""

        dlc: List[Dict[str, Any]] = []

        dlc = DLC.IDs(self, dlc)

        Utility.WriteFile(self, f"{self.eXAssets}/dlc.json", dlc)

        log.info(f"Compiled {len(dlc):,} DLC")

    def IDs(self: Any, dlc: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/dlc_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/dlc_ids.csv", DLCIDs
        )

        if ids is None:
            return dlc

        for entry in ids:
            isCP: bool = bool(entry.get("isCODPoints", 0))
            amountCP: int = 0 if (amnt := entry.get("CPAmount")) is None else int(amnt)

            dlc.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("name"),
                    "name": self.localize.get(entry.get("title"))
                    if isCP is False
                    else self.localize.get(entry.get("title")).replace(
                        "&&1", f"{amountCP:,}"
                    ),
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "altType": entry.get("type"),
                    "image": entry.get("image"),
                    "storeIds": {
                        "battlenet": entry.get("battleNetID"),
                        "playstation": entry.get("PS4ID"),
                        "xbox": entry.get("XB1ID"),
                    },
                    "items": [],
                }
            )

            if dlc[-1]["altType"] == "consumable":
                if dlc[-1].get("type") is None:
                    dlc[-1]["type"] = self.localize.get("LOOT_MP/CONSUMABLE")

                if dlc[-1].get("rarity") is None:
                    dlc[-1]["rarity"] = self.ModernWarfare.GetLootRarity(0)

            for i in range(1, 84):
                if (item := entry.get(f"item{i}")) is None:
                    continue

                dlc[-1]["items"].append(
                    {"id": item, "type": self.ModernWarfare.GetLootType(item)}
                )

        return dlc
