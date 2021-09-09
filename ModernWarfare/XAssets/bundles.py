import logging
from typing import Any, Dict, List, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class BundleIDs(TypedDict):
    """Structure of loot/bundle_ids.csv"""

    id: int
    name: str
    description: str
    flavorText: str
    license: int
    bundleType: str
    image: str
    previewImage: str
    titleImage: str
    currencyID: int
    currencyAmount: int
    saleCurrencyAmount: int
    firstPartyProductID: str
    numItems: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    item7: int
    item8: int
    item9: int
    item10: int
    numHiddenItems: int
    hiddenItem1: int
    hiddenItem2: int
    hiddenItem3: int
    hiddenItem4: int
    hiddenItem5: int
    hiddenItem6: int
    hiddenItem7: int
    hiddenItem8: int
    hiddenItem9: int
    hiddenItem10: int
    smartID: int
    smartCost: int
    isBattlePassBundle: int  # bool
    purchaseEnd: str
    dlcRef: str
    oldBundleOwnershipID: int
    isCollection: int  # bool
    ref: str
    minTierInclude: int
    maxTierInclude: int
    battlePassID: int
    collectionName: str
    collectionImage: str
    collectionPreviewImage: str
    featureText: str
    unknown1: str  # Not defined in luashared/csvutils.csv
    unknown2: str  # Not defined in luashared/csvutils.csv
    unknown3: str  # Not defined in luashared/csvutils.csv
    unknown4: str  # Not defined in luashared/csvutils.csv
    unknown5: str  # Not defined in luashared/csvutils.csv
    unknown6: str  # Not defined in luashared/csvutils.csv
    unknown7: str  # Not defined in luashared/csvutils.csv
    unknown8: str  # Not defined in luashared/csvutils.csv
    unknown9: str  # Not defined in luashared/csvutils.csv
    unknown10: str  # Not defined in luashared/csvutils.csv
    unknown11: str  # Not defined in luashared/csvutils.csv
    unknown12: str  # Not defined in luashared/csvutils.csv
    unknown13: str  # Not defined in luashared/csvutils.csv
    game: str
    giftable: int  # bool
    hasOperatorMissions: int  # bool
    mastercraft: int  # bool
    reactive: int  # bool
    ultraoutfit: int  # bool


class Bundles:
    """Bundle XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Bundle XAssets."""

        bundles: List[Dict[str, Any]] = []

        bundles = Bundles.IDs(self, bundles)

        Utility.WriteFile(self, f"{self.eXAssets}/bundles.json", bundles)

        log.info(f"Compiled {len(bundles):,} Bundles")

    def IDs(self: Any, bundles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/bundle_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/bundle_ids.csv", BundleIDs
        )

        if ids is None:
            return bundles

        for entry in ids:
            if bool(entry.get("isCollection")) is False:
                bundles.append(
                    {
                        "id": entry.get("id"),
                        "altId": entry.get("ref"),
                        "name": self.localize.get(entry.get("name")),
                        "description": self.localize.get(entry.get("description")),
                        "flavor": self.localize.get(entry.get("flavorText")),
                        "feature": self.localize.get(entry.get("featureText")),
                        "type": self.localize.get(
                            entry.get("bundleType"),
                            self.localize.get("MENU/BUNDLE_TYPE_VARIETY"),
                        ),
                        "season": self.ModernWarfare.GetLootSeason(
                            entry.get("license")
                        ),
                        "available": self.ModernWarfare.GetTitleAvailability(
                            entry.get("id")
                        ),
                        "billboard": None
                        if (i := entry.get("image")) == "placeholder_x"
                        else i,
                        "logo": None
                        if (i := entry.get("titleImage")) == "placeholder_x"
                        else i,
                        "price": None
                        if (entry.get("currencyID") != 20)
                        or ((amnt := entry.get("currencyAmount")) == 9999)
                        else amnt,
                        "salePrice": None
                        if (entry.get("currencyID") != 20)
                        or ((amnt := entry.get("saleCurrencyAmount")) == 9999)
                        else amnt,
                        "giftable": bool(entry.get("giftable")),
                        "mission": bool(entry.get("hasOperatorMissions")),
                        "mastercraft": bool(entry.get("mastercraft")),
                        "reactive": bool(entry.get("reactive")),
                        "ultraSkin": bool(entry.get("ultraoutfit")),
                        "items": [],
                        "hiddenItems": [],
                    }
                )

            for i in range(1, entry.get("numItems") + 1):
                if (item := entry.get(f"item{i}")) is None:
                    continue

                bundles[-1]["items"].append(
                    {
                        "id": item,
                        "type": self.ModernWarfare.GetLootType(item),
                    }
                )

            for i in range(1, entry.get("numHiddenItems") + 1):
                if (item := entry.get(f"hiddenItem{i}")) is None:
                    continue

                bundles[-1]["hiddenItems"].append(
                    {
                        "id": item,
                        "type": self.ModernWarfare.GetLootType(item),
                    }
                )

        return bundles
