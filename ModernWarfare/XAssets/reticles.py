import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class ReticleIDs(TypedDict):
    """Structure of loot/reticle_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class ReticleTable(TypedDict):
    """Structure of mp/reticletable.csv"""

    index: int
    ref: str
    name: str
    desc: str
    image: str
    unknown1: int  # Not defined in luashared/csvutils.lua
    hideInUI: int  # bool
    category: str
    unknown2: str  # Not defined in luashared/csvutils.lua
    unlockType: str
    unlockString: str
    availableOffline: int  # bool
    altImage: str
    flipHybridAltImage: str
    battlepassImage: str
    unlockChallengeRef: str


class Reticles:
    """Reticle XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Reticle XAssets."""

        reticles: List[Dict[str, Any]] = []

        reticles = Reticles.IDs(self, reticles)
        reticles = Reticles.Table(self, reticles)

        Utility.WriteFile(self, f"{self.eXAssets}/reticles.json", reticles)

        log.info(f"Compiled {len(reticles):,} Reticles")

    def IDs(self: Any, reticles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/reticle_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/reticle_ids.csv", ReticleIDs
        )

        if ids is None:
            return reticles

        for entry in ids:
            reticles.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("ref"),
                    "name": None,
                    "description": None,
                    "type": self.ModernWarfare.GetLootType(entry.get("id")),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("rarity")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "available": self.ModernWarfare.GetTitleAvailability(
                        entry.get("id")
                    ),
                    "hidden": None,
                    "image": None,
                    "background": "ui_loot_bg_generic",
                }
            )

        return reticles

    def Table(self: Any, reticles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/reticletable.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/reticletable.csv", ReticleTable
        )

        if table is None:
            return reticles

        for reticle in reticles:
            for entry in table:
                if reticle.get("altId") != entry.get("ref"):
                    continue

                reticle["name"] = self.localize.get(entry.get("name"))
                reticle["description"] = self.localize.get(entry.get("desc"))
                reticle["hidden"] = bool(entry.get("hideInUI"))
                reticle["image"] = entry.get("image")

        return reticles
