import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class T9UnlockItems(TypedDict):
    """Structure of loot/t9_unlock_items.csv"""

    id: int
    ref: str
    quality: int
    name: str
    description: str
    classname: str
    image: str
    imageLarge: str
    license: int  # Not defined in luashared/csvutils.lua


class UnlockItemsT9:
    """Unlock Item XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Unlock Item XAssets."""

        unlocks: List[Dict[str, Any]] = []

        unlocks = UnlockItemsT9.Table(self, unlocks)

        Utility.WriteFile(self, f"{self.eXAssets}/unlockItemsT9.json", unlocks)

        log.info(f"Compiled {len(unlocks):,} T9 Unlock Items")

    def Table(self: Any, unlocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/t9_unlock_items.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/t9_unlock_items.csv", T9UnlockItems
        )

        if table is None:
            return unlocks

        for entry in table:
            unlocks.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("name")),
                    "description": self.localize.get(entry.get("description")),
                    "type": self.localize.get(entry.get("classname")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "image": None
                    if (img := entry.get("image")) == "placeholder_x"
                    else img,
                    "background": "ui_loot_bg_generic",
                }
            )

        return unlocks
