import logging
from typing import Any, Dict, List, Optional, TypedDict

from utility import Utility

from .database import Database
from .XAssets import (
    Accessories,
    BattlePasses,
    BattlePassItems,
    Bundles,
    CallingCards,
    Camos,
    Charms,
    Consumables,
    Emblems,
    Equipment,
    Executions,
    Features,
    GameTypes,
    Gestures,
    ItemSources,
    Killstreaks,
    Maps,
    MasteryChallenges,
    MiscellaneousChallenges,
    MissionItems,
    Missions,
    OfficerChallenges,
    Operators,
    PlaylistEvents,
    ProgressionRewards,
    Quips,
    Reticles,
    SeasonalChallenges,
    SeasonalEvents,
    Skins,
    SpecialItems,
    Splashes,
    Sprays,
    Stickers,
    TurboChallenges,
    UnlockItemsT9,
    VehicleCamos,
    VehicleHorns,
    Vehicles,
    VehicleTracks,
    Weapons,
    WeaponUnlockChallenges,
    WeeklyChallengesBR,
    WeeklyChallengesMP,
)

log: logging.Logger = logging.getLogger(__name__)


class LootMaster(TypedDict):
    """Structure of loot/loot_master.csv"""

    rangeStart: int
    rangeEnd: int
    typeName: str
    typeValue: str
    hidden: int
    typeNameLoc: str
    typeDesc: str
    typeImg: str
    breadcrumb: str
    baseWeaponRef: str


class ItemSourceTable(TypedDict):
    """Structure of mp/itemsourcetable.csv"""

    marketPlaceID: int
    refType: str
    refName: str
    gameSourceID: str
    equippableIW8MP: int  # bool
    equippableWZ: int  # bool
    equippableT9: int  # bool
    equippableS4: int  # bool
    lookupType: str


class OperatorIDs(TypedDict):
    """Structure of loot/operator_ids.csv"""

    id: int
    ref: str
    rarity: int
    price: int
    salvage: int
    license: int
    premium: int  # bool


class WeaponClassTable(TypedDict):
    """Structure of mp/weaponClassTable.csv"""

    index: int
    ref: str
    slot: int
    name: str
    pluralName: str
    showInMenus: int  # bool
    unlockTablePrefix: str
    showInCP: int  # bool
    image: str
    showInArmory: int  # bool
    previewScene: str
    attachScenePrefix: str
    unknown1: str  # Not defined in luashared/csvutils.csv
    unknown2: str  # Not defined in luashared/csvutils.csv
    classImage: str
    canBeGunsmithed: int  # bool
    attachCategoryWhitelist: str  # Array of strings
    hasVariants: int  # bool
    isWZOnly: int  # bool


class AttachmentCategoryTable(TypedDict):
    """Structure of mp/attachmentcategorytable.csv"""

    index: int
    ref: str
    name: str
    buttonIndex: int
    displayOrder: int
    categoryScene: str
    smallCategoryScene: str
    largeCategoryScene: str
    bone: str
    defaultLineOffsetX: int
    defaultLineOffsetY: int
    defaultLineOffsetZ: int
    enableBigGunPreviewCamera: int  # bool
    enableSmallGunPreviewCamera: int  # bool
    enableBigShotgunPreviewCamera: int  # bool


class CamoCategoryTable(TypedDict):
    """Structure of mp/camocategorytable.csv"""

    index: int
    ref: str
    name: str


class ModernWarfare:
    """Call of Duty: Modern Warfare (IW8)"""

    def __init__(self: Any, config: dict) -> None:
        self.ModernWarfare = self

        self.config: Dict[str, Any] = config.get("ModernWarfare")
        self.iXAssets: str = self.config["import"]["xassets"]
        self.iImages: str = self.config["import"]["images"]
        self.iVideos: str = self.config["import"]["videos"]
        self.eXAssets: str = self.config["export"]["xassets"]
        self.eImages: str = self.config["export"]["images"]
        self.eVideos: str = self.config["export"]["videos"]
        self.eDatabase: str = self.config["export"]["database"]

    def Compile(self: Any) -> None:
        """Compile and export all supported XAsset types for Modern Warfare."""

        log.info("Compiling XAssets for Call of Duty: Modern Warfare...")

        # Global and reused XAssets
        self.localize: Dict[str, Optional[str]] = ModernWarfare.LoadLocalize(self)
        self.lootTypes: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/loot_master.csv", LootMaster, 1
        )
        self.itemSources: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/itemsourcetable.csv", ItemSourceTable
        )
        self.operatorIds: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/operator_ids.csv", OperatorIDs
        )
        self.weaponClasses: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/weaponClassTable.csv", WeaponClassTable
        )
        self.attachCategories: List[Dict[str, Any]] = Utility.ReadCSV(
            self,
            f"{self.iXAssets}/mp/attachmentcategorytable.csv",
            AttachmentCategoryTable,
        )
        self.camoCategories: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/camocategorytable.csv", CamoCategoryTable
        )

        Accessories.Compile(self)
        BattlePasses.Compile(self)
        BattlePassItems.Compile(self)
        Bundles.Compile(self)
        CallingCards.Compile(self)
        Camos.Compile(self)
        Charms.Compile(self)
        Consumables.Compile(self)
        Emblems.Compile(self)
        Equipment.Compile(self)
        Executions.Compile(self)
        Features.Compile(self)
        GameTypes.Compile(self)
        Gestures.Compile(self)
        ItemSources.Compile(self)
        Killstreaks.Compile(self)
        Maps.Compile(self)
        MasteryChallenges.Compile(self)
        MiscellaneousChallenges.Compile(self)
        MissionItems.Compile(self)
        Missions.Compile(self)
        OfficerChallenges.Compile(self)
        Operators.Compile(self)
        PlaylistEvents.Compile(self)
        ProgressionRewards.Compile(self)
        Quips.Compile(self)
        Reticles.Compile(self)
        SeasonalChallenges.Compile(self)
        SeasonalEvents.Compile(self)
        Skins.Compile(self)
        SpecialItems.Compile(self)
        Splashes.Compile(self)
        Sprays.Compile(self)
        Stickers.Compile(self)
        TurboChallenges.Compile(self)
        UnlockItemsT9.Compile(self)
        VehicleCamos.Compile(self)
        VehicleHorns.Compile(self)
        Vehicles.Compile(self)
        VehicleTracks.Compile(self)
        Weapons.Compile(self)
        WeaponUnlockChallenges.Compile(self)
        WeeklyChallengesBR.Compile(self)
        WeeklyChallengesMP.Compile(self)

        if self.config.get("compileDatabase") is True:
            Database.Compile(self)

    def LoadLocalize(self: Any) -> Dict[str, Optional[str]]:
        """Load and filter the localized string entries for Modern Warfare."""

        localize: Dict[str, Optional[str]] = Utility.ReadFile(
            self, f"{self.iXAssets}/localize.json"
        )
        placeholders: dict = Utility.ReadFile(self, "ModernWarfare/placeholders.json")

        for key in localize:
            value: Optional[str] = localize.get(key)

            if value is None:
                continue

            for placeholder in placeholders.get("whole"):
                if value.lower() == placeholder.lower():
                    localize[key] = None

                    break

            for placeholder in placeholders.get("begins"):
                if value.lower().startswith(placeholder.lower()) is True:
                    localize[key] = None

                    break

            for placeholder in placeholders.get("ends"):
                if value.lower().endswith(placeholder.lower()) is True:
                    localize[key] = None

                    break

            if (value := localize.get(key)) is not None:
                value = Utility.StripColorCodes(self, value)
                value = Utility.StripButtonCodes(self, value)

                localize[key] = value

        return localize

    def GetLootRarity(self: Any, value: int) -> Optional[str]:
        """Get the loot rarity for the provided value."""

        return self.localize.get(f"LOOT_MP/QUALITY_{value}")

    def GetLootType(self: Any, id: int) -> Optional[str]:
        """Get the loot type for the provided id."""

        if id is None:
            return

        for loot in self.lootTypes:
            start: int = loot.get("rangeStart")
            end: int = loot.get("rangeEnd")

            if (id >= start) and (id <= end):
                typeNameLoc: Optional[str] = loot.get("typeNameLoc")

                if typeNameLoc == "LOOT_MP/PLACEHOLDER":
                    break

                return self.localize.get(typeNameLoc)

        for source in self.itemSources:
            if source.get("marketPlaceID") == id:
                refType: Optional[str] = source.get("refType")

                # Partially defined in ui/utils/lootutils.lua
                if refType == "weapon":
                    return self.localize.get("LOOT_MP/ITEM_TYPE_WEAPON")
                elif refType == "operator":
                    return self.localize.get("LOOT_MP/OPERATOR")
                elif refType == "operator_skin":
                    return self.localize.get("LOOT_MP/OPERATOR_SKIN")
                elif refType == "executions":
                    return self.localize.get("LOOT_MP/OPERATOR_EXECUTION")
                elif refType == "equipment":
                    return self.localize.get("LOOT_MP/EQUIPMENT")
                elif refType == "accessory":
                    return self.localize.get("LOOT_MP/WATCH")
                elif refType == "playercards":
                    return self.localize.get("LOOT_MP/CALLING_CARD")
                elif refType == "weapon_charm":
                    return self.localize.get("LOOT_MP/CHARM")
                elif refType == "quip":
                    return self.localize.get("LOOT_MP/OPERATOR_QUIP")
                elif refType == "camo":
                    return self.localize.get("LOOT_MP/CAMO")
                elif refType == "emblems":
                    return self.localize.get("LOOT_MP/EMBLEM")
                elif refType == "attachment":
                    return self.localize.get("LOOT_MP/ATTACHMENT")
                elif refType == "sticker":
                    return self.localize.get("LOOT_MP/STICKER")
                elif refType == "xp_token":
                    return self.localize.get("LOOT_MP/CONSUMABLE")
                elif refType == "markeritem":
                    return self.localize.get("LOOT_MP/CONSUMABLE")
                elif refType == "reticle":
                    return self.localize.get("LOOT_MP/RETICLE")
                elif refType == "blueprint":
                    return self.localize.get("LOOT_MP/ITEM_TYPE_WEAPON")
                elif refType == "battlepass":
                    return self.localize.get("LOOT_MP/BATTLE_PASS")
                elif refType == "vehicle_track":
                    return self.localize.get("LOOT_MP/VEHICLE_TRACK")
                elif refType == "vehicle_horn":
                    return self.localize.get("LOOT_MP/VEHICLE_HORN")
                elif refType == "feature":
                    return self.localize.get("LOOT_MP/FEATURE")
                elif refType == "weapon_attachment":
                    return self.localize.get("LOOT_MP/ATTACHMENT")
                elif refType == "perk":
                    return self.localize.get("LOOT_MP/PERK")
                elif refType == "t9_equipment":
                    return self.localize.get("LOOT_MP/EQUIPMENT")
                elif refType == "killstreak":
                    return self.localize.get("LOOT_MP/STREAK")
                elif refType == "class":
                    return self.localize.get("LOOT_MP/FEATURE")
                elif refType == "zm_unlockable":
                    return self.localize.get("LOOT_MP/FEATURE")
                elif refType == "weapon_skill":
                    return self.localize.get("LOOT_MP/FEATURE")
                elif refType == "bonuscard":
                    return self.localize.get("LOOT_MP/FEATURE")
                elif refType == "vehicleskin":
                    return self.localize.get("LOOT_MP/VEHICLE_SKIN")
                elif refType == "bundle":
                    return self.localize.get("MENU/BUNDLE_TYPE_VARIETY")
                elif refType == "placeholder":
                    return
                else:
                    log.warning(
                        f"Found unknown Loot Type; ID: {id}, refType: {refType}"
                    )

    def GetLootSeason(self: Any, license: int) -> Optional[str]:
        """Get the loot season for the provided value."""

        if license == 0:
            return
        elif license == 99:
            # Defined in ui/utils/lootutils.lua
            return "Unreleased"
        elif ((license - 1) % 1000) == 0:
            # For instances such as the Season 4: Reloaded update.
            license -= 1
        elif ((license - 2) % 1000) == 0:
            # For instances such as the Season 6 extension.
            license -= 2
        elif (license % 1000) != 0:
            # Seasonal licenses are multiples of 1,000.
            return

        return self.localize.get(f"SEASONS/SEASON_{round(license / 1000)}")

    def GetOperatorID(self: Any, reference: str) -> Optional[int]:
        """Get the ID for the specified Operator."""

        if reference == "universal_ref":
            # Universal Operator items do not have an ID, so we'll just
            # set one ourselves.
            return 29999
        elif reference == "universal_base_ref":
            # Same reason as universal_ref, however, this is only intended
            # for use with Operators where isLaunchOperator is True.
            return 29998
        elif reference == "t9_exclusive_ref":
            # Same reason as universal_ref, however, this is only intended
            # for use with Black Ops Cold War Operators.
            return 29997

        for operator in self.operatorIds:
            if reference == operator.get("ref"):
                return operator.get("id")

    def GetWeaponClass(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified Weapon Class."""

        for weaponClass in self.weaponClasses:
            if reference == weaponClass.get("ref"):
                return self.localize.get(weaponClass.get("name"))

    def GetAttachmentCategory(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified attachment category."""

        for category in self.attachCategories:
            if category.get("ref") == reference:
                return self.localize.get(category.get("name"))

    def GetCamoCategory(self: Any, reference: str) -> Optional[str]:
        """Get the name of the specified camo category."""

        for category in self.camoCategories:
            if category.get("ref") == reference:
                return self.localize.get(category.get("name"))

    def GetAttribute(self: Any, reference: str) -> Optional[str]:
        """
        Get the name of the specified attribute.

        Defined in ui/utils/weaponutils.lua and ui/utils/vehicleutils.lua
        """

        attributes: Dict[str, str] = {
            "red": "WEAPON/TRACER_RED",
            "blue": "WEAPON/TRACER_BLUE",
            "pink": "WEAPON/TRACER_PINK",
            "green": "WEAPON/TRACER_GREEN",
            "purple": "WEAPON/TRACER_PURPLE",
            "freedom": "WEAPON/TRACER_FREEDOM",
            "shadow": "WEAPON/TRACER_SHADOW",
            "gold": "WEAPON/TRACER_GOLD",
            "morte": "WEAPON/TRACER_MORTE",
            "tesla": "WEAPON/TRACER_TESLA",
            "sixteenBit": "WEAPON/TRACER_16BIT",
            "dark": "WEAPON/TRACER_DARK",
            "light": "WEAPON/TRACER_LIGHT",
            "orange": "WEAPON/TRACER_ORANGE",
            "yellow": "WEAPON/TRACER_YELLOW",
            "soul": "WEAPON/TRACER_SOUL",
            "purpleGreen": "WEAPON/TRACER_PURPLE_GREEN",
            "standardDis": "WEAPON/DISMEMBERMENT",
            "cryoDis": "WEAPON/CRYO_DISMEMBERMENT",
            "goldDis": "WEAPON/DISMEMBERMENT_GOLD",
            "electricDis": "WEAPON/DISMEMBERMENT_ELECTRIC",
            "tailLightTracerRed": "VEHICLES/ATTRIBUTE_TAIL_LIGHT_TRACER_RED",
            "flightTrailStandard": "VEHICLES/ATTRIBUTE_FLIGHT_TRAIL_STANDARD",
            "flightTrailShadow": "VEHICLES/ATTRIBUTE_FLIGHT_TRAIL_SHADOW",
            "tireTrailFlame": "VEHICLES/ATTRIBUTE_TIRE_TRAIL_FLAME",
            "smoke": "VEHICLES/ATTRIBUTE_SMOKE",
            "tireTrailTesla": "VEHICLES/ATTRIBUTE_TIRE_TRAIL_TESLA",
            "crimsonGold": "WEAPON/TRACER_CRIMSON_GOLD",
            "emerald": "WEAPON/TRACER_EMERALD",
            "amethyst": "WEAPON/TRACER_AMETHYST",
            "cherryBlossom": "WEAPON/TRACER_CHERRY_BLOSSOM",
            "ice": "WEAPON/TRACER_ICE",
            "rainbow": "WEAPON/TRACER_RAINBOW",
            "black": "WEAPON/TRACER_BLACK",
            "crimsonRonin": "WEAPON/TRACER_CRIMSON_RONIN",
            "acid": "WEAPON/TRACER_ACID",
            "tailLightTracerAkira": "VEHICLES/ATTRIBUTE_TAIL_LIGHT_TRACER_AKIRA",
            "flightTrailRainbow": "VEHICLES/ATTRIBUTE_FLIGHT_TRAIL_RAINBOW",
        }

        return self.localize.get(attributes.get(reference))

    def GetGameTypeCategory(self: Any, reference: str) -> Optional[str]:
        """
        Get the name of the specified game type category.

        Defined in ui/utils/mplobbyutils.lua and ui/frontend/mp/gamemodes.lua
        """

        categories: Dict[str, str] = {
            "PrivateTournament": "LUA_MENU/TOURNAMENT",
            "Plunder": "LUA_MENU/GAMEMODE_PLUNDER",
            "BattleRoyale": "LUA_MENU/GAMEMODE_BATTLE_ROYALE",
            "WarzoneAlternate": "LUA_MENU/GAMEMODE_WARZONE_ALTERNATE",
            "MyModes": "LUA_MENU/MY_MODES",
            "Cwl": "LUA_MENU/CWL_MODES",
            "Standard": "LUA_MENU/STANDARD_MODES",
            "Alternate": "LUA_MENU/ALTERNATE_MODES",
        }

        return self.localize.get(categories.get(reference))

    def GetPlatformExclusivity(self: Any, reference: str) -> str:
        """
        Get the name of the specified platform.

        Defined in ui/utils/lui.lua
        """

        if reference is None:
            return
        elif reference == "pc":
            return "battlenet"
        elif reference == "sy":
            return "playstation"
        elif reference == "ms":
            return "xbox"

    def GetTitleAvailability(self: Any, id: int) -> Dict[str, bool]:
        """Get the title availability for the specified item."""

        for item in self.itemSources:
            if id == item.get("marketPlaceID"):
                return {
                    "coldWar": bool(item.get("equippableT9")),
                    "warzone": bool(item.get("equippableWZ")),
                    "modernWarfare": bool(item.get("equippableIW8MP")),
                }

        return {"coldWar": False, "warzone": True, "modernWarfare": True}
