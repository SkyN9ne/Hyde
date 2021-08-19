import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class BRKioskPurchases(TypedDict):
    """Structure of mp/brkioskpurchases.csv"""

    index: int
    type: str
    ref: str
    cost: int
    title: str
    desc: str
    icon: str
    tabNum: int
    slotLabel: str
    fireSaleDiscount: int
    perkDiscount: int
    overrideFileOnly: int  # bool


class BRKioskPurchasesTruckWar(TypedDict):
    """Structure of mp/brkioskpurchases_truckwar.csv"""

    index: int
    type: str
    ref: str
    cost: int
    title: str
    desc: str
    icon: str
    tabNum: int
    slotLabel: str
    fireSaleDiscount: int
    perkDiscount: int
    overrideFileOnly: int  # bool


class KioskBR:
    """Battle Royale Kiosk Purchases XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Battle Royale Kiosk Purchases XAssets."""

        items: List[Dict[str, Any]] = []

        items = KioskBR.IDs(self, items)

        Utility.WriteFile(self, f"{self.eXAssets}/kioskBR.json", items)

        log.info(f"Compiled {len(items):,} Kiosk Items (BR)")

    def IDs(self: Any, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/brkioskpurchases.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self,
            f"{self.iXAssets}/mp/brkioskpurchases.csv",
            BRKioskPurchasesTruckWar,
        )

        if ids is None:
            return items

        for entry in ids:
            items.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("title")),
                    "description": self.localize.get(entry.get("desc")),
                    "label": self.localize.get(entry.get("slotLabel")),
                    "type": entry.get("type"),
                    "price": entry.get("cost") * 100,
                    "image": entry.get("icon"),
                }
            )

        return items


class KioskBRTruck:
    """Battle Royale Kiosk Purchases (Truck War) XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Battle Royale Kiosk Purchases (Truck War) XAssets."""

        items: List[Dict[str, Any]] = []

        items = KioskBRTruck.IDs(self, items)

        Utility.WriteFile(self, f"{self.eXAssets}/kioskBRTruck.json", items)

        log.info(f"Compiled {len(items):,} Kiosk Items (BR Truck War)")

    def IDs(self: Any, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/brkioskpurchases_truckwar.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self,
            f"{self.iXAssets}/mp/brkioskpurchases_truckwar.csv",
            BRKioskPurchasesTruckWar,
        )

        if ids is None:
            return items

        for entry in ids:
            items.append(
                {
                    "altId": entry.get("ref"),
                    "name": self.localize.get(entry.get("title")),
                    "description": self.localize.get(entry.get("desc")),
                    "label": self.localize.get(entry.get("slotLabel")),
                    "type": entry.get("type"),
                    "price": entry.get("cost") * 100,
                    "image": entry.get("icon"),
                }
            )

        return items
