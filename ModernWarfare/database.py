import logging
from typing import Any, Dict, List, Optional

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class Database:
    """
    XAssets used in the COD Tracker Database.
    https://cod.tracker.gg/warzone/db
    """

    def Compile(self: Any) -> None:
        """Compile the XAssets for the COD Tracker Database."""

        self.dbImages: List[str] = []
        self.count: int = 0

        DBBattlePasses.Compile(self)
        DBBundles.Compile(self)
        DBLoot.Compile(self)
        DBOperators.Compile(self)
        DBWeapons.Compile(self)

        imgChunk: str = ""
        imgWhole: str = ""

        for image in set(self.dbImages):
            if (len(imgChunk) + len(f"{image},")) < 30000:
                imgChunk += f"{image},"
            else:
                # Don't ask
                imgWhole += f"{imgChunk}\n\n\n\n\n\n\n\n\n\n"
                imgChunk = f"{image},"

        if (len(imgWhole) == 0) and (len(imgChunk) > 0):
            imgWhole = imgChunk

        Utility.WriteFile(self, f"{self.eDatabase}/_images.txt", imgWhole)

        log.info(f"Compiled {self.count:,} Database Items")


class DBBattlePasses:
    """Battle Pass XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Battle Pass XAssets for the COD Tracker Database."""

        dbPasses: List[Dict[str, Any]] = []
        passes: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/battlePasses.json"
        )

        for battlePass in passes:
            if battlePass.get("name") is None:
                continue

            items: List[Dict[str, Any]] = []

            for item in battlePass.get("items"):
                item.pop("type")
                item.pop("billboard")

                items.append(item)

            dbPasses.append(battlePass)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/battlePasses.json",
            dbPasses,
            compress=True,
        )
        Utility.WriteFile(self, f"{self.eDatabase}/_battlePasses.json", dbPasses)


class DBBundles:
    """Bundle XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Bundle XAssets for the COD Tracker Database."""

        dbBundles: List[Dict[str, Any]] = []
        bundles: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/bundles.json"
        )
        dlc: List[Dict[str, Any]] = Utility.ReadFile(self, f"{self.eXAssets}/dlc.json")

        for bundle in bundles:
            if bundle.get("id") is None:
                continue
            elif bundle.get("name") is None:
                continue
            elif bundle.get("type") is None:
                continue
            elif (b := bundle.get("billboard")) is None:
                continue
            elif (l := bundle.get("logo")) is None:
                continue

            self.dbImages.append(b)
            self.dbImages.append(l)

            if Utility.FileExists(self, f"{self.iImages}/{b}.png") is False:
                continue
            elif Utility.FileExists(self, f"{self.iImages}/{l}.png") is False:
                continue

            items: List[int] = []

            for item in bundle.get("items"):
                items.append(item.get("id"))

            bundle["items"] = items

            bundle.pop("altId")
            bundle.pop("giftable")
            bundle.pop("mission")
            bundle.pop("mastercraft")
            bundle.pop("reactive")
            bundle.pop("ultraSkin")
            bundle.pop("hiddenItems")

            if bundle.get("description") is None:
                bundle.pop("description")
            if bundle.get("flavor") is None:
                bundle.pop("flavor")
            if bundle.get("feature") is None:
                bundle.pop("feature")
            if bundle.get("season") is None:
                bundle.pop("season")
            if bundle.get("salePrice") is None:
                bundle.pop("salePrice")
            if bundle.get("name") == bundle.get("flavor"):
                bundle.pop("flavor")
            if bundle.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": True,
                "modernWarfare": True,
            }:
                bundle.pop("available", None)
            if bundle.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": False,
                "modernWarfare": False,
            }:
                bundle.pop("available", None)

            if Utility.AnimateSprite(self, b, [(1920, 580)]) is True:
                bundle["animated"] = True

            bundle["slug"] = Utility.Sluggify(self, bundle.get("name"))

            dbBundles.append(bundle)
            self.count += 1

        for entry in dlc:
            if entry.get("altType") != "durable":
                continue

            if entry.get("id") is None:
                continue
            elif entry.get("name") is None:
                continue
            elif (b := entry.get("image")) is None:
                continue

            self.dbImages.append(b)

            if Utility.FileExists(self, f"{self.iImages}/{b}.png") is False:
                continue

            items: List[int] = []

            for item in entry.get("items"):
                if item.get("type") == self.localize.get("LOOT_MP/OPERATOR"):
                    continue

                items.append((itemId := item.get("id")))

                for bundle in bundles:
                    if itemId == bundle.get("id"):
                        items.remove(itemId)

                        break

            entry["items"] = items

            entry.pop("altId", None)
            entry.pop("altType", None)
            entry.pop("storeIds", None)
            entry.pop("image", None)

            entry["billboard"] = b
            entry["price"] = None

            if entry.get("type") is None:
                entry["type"] = self.localize.get("MENU/BUNDLE_TYPE_VARIETY")

            if Utility.AnimateSprite(self, b, [(1920, 580)]) is True:
                entry["animated"] = True

            entry["slug"] = Utility.Sluggify(self, entry.get("name"))

            dbBundles.append(entry)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/bundles.json",
            Utility.SortList(self, dbBundles, "name", key2="type"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_bundles.json",
            Utility.SortList(self, dbBundles, "name", key2="type"),
        )


class DBLoot:
    """Loot XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Loot XAssets for the COD Tracker Database."""

        dbLoot: List[Dict[str, Any]] = []
        loot: List[str] = [
            "accessories",
            "battlePassItems",
            "callingCards",
            "camos",
            "charms",
            "consumables",
            "dlc",
            "emblems",
            "executions",
            "features",
            "gestures",
            "missionItems",
            "operatorQuips",
            "operatorSkins",
            "reticles",
            "specialItems",
            "sprays",
            "stickers",
            "unlockItemsT9",
            "vehicleCamos",
            "vehicleHorns",
            "vehicleTracks",
        ]

        for file in loot:
            items: List[Dict[str, Any]] = Utility.ReadFile(
                self, f"{self.eXAssets}/{file}.json"
            )

            for item in items:
                if item.get("id") is None:
                    continue
                elif item.get("name") is None:
                    continue
                elif item.get("type") is None:
                    continue
                elif item.get("rarity") is None:
                    continue
                elif (i := item.get("image")) is None:
                    continue

                if (file == "dlc") and (item.get("altType") != "consumable"):
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                item.pop("altId", None)
                item.pop("altType", None)
                item.pop("hidden", None)
                item.pop("category", None)
                item.pop("operatorAltId", None)
                item.pop("pet", None)
                item.pop("unlock", None)
                item.pop("sku", None)
                item.pop("rewards", None)
                item.pop("challengeId", None)
                item.pop("storeIds", None)
                item.pop("items", None)

                if item.get("description") is None:
                    item.pop("description", None)
                if item.get("flavor") is None:
                    item.pop("flavor", None)
                if item.get("season") is None:
                    item.pop("season", None)
                if item.get("season") == "Unreleased":
                    item.pop("season", None)
                if item.get("attribute") is None:
                    item.pop("attribute", None)
                if item.get("exclusive") is None:
                    item.pop("exclusive", None)
                if item.get("available") == {
                    "vanguard": False,
                    "coldWar": False,
                    "warzone": True,
                    "modernWarfare": True,
                }:
                    item.pop("available", None)
                if item.get("available") == {
                    "vanguard": False,
                    "coldWar": False,
                    "warzone": False,
                    "modernWarfare": False,
                }:
                    item.pop("available", None)

                if (iType := item.get("type")) == "Calling Card":
                    if (
                        Utility.AnimateSprite(
                            self, i, [(512, 128), (512, 136), (960, 240)]
                        )
                        is True
                    ):
                        item["animated"] = True
                elif iType == "Emblem":
                    if Utility.AnimateSprite(self, i, [(256, 256)]) is True:
                        item["animated"] = True

                item["slug"] = Utility.Sluggify(self, item.get("name"))

                if item in dbLoot:
                    continue

                dbLoot.append(item)
                self.count += 1

        weapons: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/weapons.json"
        )

        for weapon in weapons:
            for variant in weapon.get("variants"):
                if variant.get("id") is None:
                    continue
                elif variant.get("name") is None:
                    continue
                elif variant.get("type") is None:
                    continue
                elif (i := variant.get("image")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                variant.pop("altId")

                if variant.get("flavor") is None:
                    variant.pop("flavor")
                if variant.get("season") is None:
                    variant.pop("season")
                if variant.get("tracers") is None:
                    variant.pop("tracers")
                if variant.get("dismemberment") is None:
                    variant.pop("dismemberment")
                if variant.get("season") == "Unreleased":
                    variant.pop("season", None)
                if variant.get("available") == {
                    "vanguard": False,
                    "coldWar": False,
                    "warzone": True,
                    "modernWarfare": True,
                }:
                    variant.pop("available", None)
                if variant.get("available") == {
                    "vanguard": False,
                    "coldWar": False,
                    "warzone": False,
                    "modernWarfare": False,
                }:
                    variant.pop("available", None)

                variant["class"] = weapon.get("class")
                variant["baseId"] = weapon.get("id")
                variant["slug"] = Utility.Sluggify(self, variant.get("name"))

                if Utility.AnimateSprite(self, i, [(300, 400)]) is True:
                    variant["animated"] = True

                dbLoot.append(variant)
                self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/loot.json",
            Utility.SortList(self, dbLoot, "name", key2="rarity"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_loot.json",
            Utility.SortList(self, dbLoot, "name", key2="rarity"),
        )


class DBOperators:
    """Operator XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Operator XAssets for the COD Tracker Database."""

        dbOperators: List[Dict[str, Any]] = []
        operators: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operators.json"
        )
        skins: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operatorSkins.json"
        )
        executions: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/executions.json"
        )
        quips: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/operatorQuips.json"
        )

        for operator in operators:
            if operator.get("id") is None:
                continue
            elif operator.get("name") is None:
                continue
            elif operator.get("type") is None:
                continue
            elif (i := operator.get("image")) is None:
                continue

            self.dbImages.append(i)

            if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                continue

            operator["skins"] = []
            operator["executions"] = []
            operator["quips"] = []
            operator["slug"] = Utility.Sluggify(self, operator.get("name"))

            for skin in Utility.SortList(self, skins, "name", key2="rarity"):
                if (skinId := skin.get("id")) is None:
                    continue
                elif skin.get("name") is None:
                    continue
                elif (i := skin.get("image")) is None:
                    continue
                elif (skinOpId := skin.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if skinOpId == operator.get("id"):
                    operator["skins"].append(skinId)
                elif (skinOpId == 29999) and (
                    operator.get("altId").startswith("t9") is False
                ):
                    operator["skins"].append(skinId)
                elif (skinOpId == 29998) and (
                    operator.get("altId").startswith("t9") is False
                ):
                    if operator.get("launchOperator") is True:
                        operator["skins"].append(skinId)

            for execution in Utility.SortList(self, executions, "name", key2="rarity"):
                if (exId := execution.get("id")) is None:
                    continue
                elif execution.get("name") is None:
                    continue
                elif (i := execution.get("image")) is None:
                    continue
                elif (exOpId := execution.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if exOpId == operator.get("id"):
                    operator["executions"].append(exId)
                elif (exOpId == 29999) and (
                    operator.get("altId").startswith("t9") is False
                ):
                    operator["executions"].append(exId)
                elif exOpId == 29997:
                    if operator.get("altId").startswith("t9") is True:
                        operator["executions"].append(exId)

            for quip in Utility.SortList(self, quips, "name", key2="rarity"):
                if (quipId := quip.get("id")) is None:
                    continue
                elif quip.get("name") is None:
                    continue
                elif (i := quip.get("image")) is None:
                    continue
                elif (quipOpId := quip.get("operatorId")) is None:
                    continue

                self.dbImages.append(i)

                if Utility.FileExists(self, f"{self.iImages}/{i}.png") is False:
                    continue

                if quipOpId == operator.get("id"):
                    operator["quips"].append(quipId)
                elif (quipOpId == 29999) and (
                    operator.get("altId").startswith("t9") is False
                ):
                    operator["quips"].append(quipId)

            operator.pop("altId")
            operator.pop("type")
            operator.pop("rarity")
            operator.pop("branchIcon")
            operator.pop("thumbprint")
            operator.pop("launchOperator")
            operator.pop("video")
            operator.pop("hidden")
            operator.pop("billets")

            if operator.get("season") is None:
                operator.pop("season")
            if operator.get("description") is None:
                operator.pop("description")
            if operator.get("branch") is None:
                operator.pop("branch")
            if operator.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": True,
                "modernWarfare": True,
            }:
                operator.pop("available", None)
            if operator.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": False,
                "modernWarfare": False,
            }:
                operator.pop("available", None)

            dbOperators.append(operator)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/operators.json",
            Utility.SortList(self, dbOperators, "name", key2="faction"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_operators.json",
            Utility.SortList(self, dbOperators, "name", key2="faction"),
        )


class DBWeapons:
    """Weapon XAssets for the COD Tracker Database."""

    def Compile(self: Any) -> None:
        """Compile the Weapon XAssets for the COD Tracker Database."""

        dbWeapons: List[Dict[str, Any]] = []
        weapons: List[Dict[str, Any]] = Utility.ReadFile(
            self, f"{self.eXAssets}/weapons.json"
        )

        for weapon in weapons:
            if weapon.get("id") is None:
                continue
            if weapon.get("name") is None:
                continue
            if weapon.get("type") is None:
                continue
            if (ico := weapon.get("icon")) is None:
                continue

            self.dbImages.append(ico)

            variants: List[int] = []

            for variant in Utility.SortList(
                self, weapon.get("variants"), "name", key2="rarity"
            ):
                if variant.get("id") is None:
                    continue
                elif variant.get("name") is None:
                    continue
                elif variant.get("type") is None:
                    continue
                elif variant.get("image") is None:
                    continue

                variants.append(variant.get("id"))

            weapon["variants"] = variants

            weapon.pop("maxAttachments")
            weapon.pop("attachments")
            weapon.pop("image")

            if weapon.get("description") is None:
                weapon.pop("description")
            if ((s := weapon.get("season")) is None) or (s == "Unreleased"):
                weapon.pop("season")
            if weapon.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": True,
                "modernWarfare": True,
            }:
                weapon.pop("available", None)
            if weapon.get("available") == {
                "vanguard": False,
                "coldWar": False,
                "warzone": False,
                "modernWarfare": False,
            }:
                weapon.pop("available", None)

            weapon["slug"] = Utility.Sluggify(self, weapon.get("name"))

            dbWeapons.append(weapon)
            self.count += 1

        Utility.WriteFile(
            self,
            f"{self.eDatabase}/weapons.json",
            Utility.SortList(self, dbWeapons, "name", key2="altName"),
            compress=True,
        )
        Utility.WriteFile(
            self,
            f"{self.eDatabase}/_weapons.json",
            Utility.SortList(self, dbWeapons, "name", key2="altName"),
        )
