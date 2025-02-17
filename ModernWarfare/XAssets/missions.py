import logging
from typing import Any, Dict, List, Optional, TypedDict

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class QuestChallenges(TypedDict):
    """Structure of quest_challenges.csv"""

    id: int
    ref: str
    name: str
    desc: str
    image: str
    category: str
    amount: int
    challenges: str
    xp: int
    loot: int
    keys: str
    salvage: str
    codPoints: str
    detailDesc: str
    totalStageValue: int
    isFinalStage: int  # bool
    activationType: int
    season: int
    unknown1: str


class IntelChallenges(TypedDict):
    """Structure of mp/intel_challenges.csv"""

    ref: str
    masterRef: str
    seasonWeek: int
    inGame: int  # bool
    event: str
    modelPartName: str
    originX: float
    originY: float
    originZ: float
    anglesX: float
    anglesY: float
    anglesZ: float
    image: str
    collectAll: int  # bool


class MissionIDs(TypedDict):
    """Structure of loot/mission_ids.csv"""

    index: int
    ref: int
    quality: int
    cost: int
    salvage: int
    license: int
    isPremium: int  # bool
    operatorSkinID: int
    missionImage: str
    missionName: str
    missionRef: str
    operatorRef: str
    operatorMissionItemID: int


class BRMissionsTable(TypedDict):
    """Structure of mp/brmissions.csv"""

    index: int
    ref: str
    title: str
    description: str
    descriptionParam: int
    paramText: str
    icon: str
    reward: str
    hasTimer: int  # bool
    paramKey: str
    useDescParamInParamText: int  # bool
    lootRef: str
    extraRewardText: str
    mapKeyIcon: str
    mapKeyTitle: str
    aarIcon: str
    overrideColor: str
    altTrackerText: str


class Missions:
    """Mission XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Mission XAssets."""

        missions: List[Dict[str, Any]] = []

        missions = Missions.QuestTable(self, missions)
        missions = Missions.IntelTable(self, missions)

        Utility.WriteFile(self, f"{self.eXAssets}/missions.json", missions)

        log.info(f"Compiled {len(missions):,} Missions")

    def QuestTable(self: Any, missions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the quest_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/quest_challenges.csv", QuestChallenges
        )

        if table is None:
            return missions

        last: Optional[str] = None

        for entry in table:
            if entry.get("name") != last:
                missions.append(
                    {
                        "id": entry.get("id"),
                        "name": self.localize.get(entry.get("name")),
                        "description": self.localize.get(entry.get("detailDesc")),
                        "category": entry.get("category"),
                        "season": self.ModernWarfare.GetLootSeason(
                            entry.get("season") * 1000
                        ),
                        "image": entry.get("image"),
                        "objectives": [
                            {
                                "altId": entry.get("ref"),
                                "description": self.localize.get(entry.get("desc")),
                                "xp": entry.get("xp"),
                                "rewards": [],
                            }
                        ],
                    }
                )

                last = entry.get("name")
            else:
                missions[-1]["objectives"].append(
                    {
                        "altId": entry.get("ref"),
                        "description": self.localize.get(entry.get("desc")),
                        "xp": entry.get("xp"),
                        "rewards": [],
                    }
                )

            if (loot := entry.get("loot")) is not None:
                missions[-1]["objectives"][-1]["rewards"].append(
                    {
                        "id": loot,
                        "type": self.ModernWarfare.GetLootType(loot),
                    }
                )

            if (desc := missions[-1]["objectives"][-1].get("description")) is not None:
                missions[-1]["objectives"][-1]["description"] = desc.replace(
                    "&&1", str(entry.get("amount"))
                )

        return missions

    def IntelTable(self: Any, missions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/intel_challenges.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/intel_challenges.csv", IntelChallenges
        )

        if table is None:
            return missions

        for mission in missions:
            for objective in mission.get("objectives", []):
                for entry in table:
                    if objective.get("altId") != entry.get("ref"):
                        continue

                    objective["image"] = entry.get("image")

        return missions


class MissionItems:
    """Mission Item XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Mission Item XAssets."""

        items: List[Dict[str, Any]] = []

        items = MissionItems.IDs(self, items)

        Utility.WriteFile(self, f"{self.eXAssets}/missionItems.json", items)

        log.info(f"Compiled {len(items):,} Mission Items")

    def IDs(self: Any, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the loot/mission_ids.csv XAsset."""

        ids: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/loot/mission_ids.csv", MissionIDs
        )

        if ids is None:
            return items

        for entry in ids:
            items.append(
                {
                    "id": entry.get("operatorMissionItemID"),
                    "altId": entry.get("missionRef"),
                    "name": self.localize.get(entry.get("missionName")),
                    "type": self.ModernWarfare.GetLootType(
                        entry.get("operatorMissionItemID")
                    ),
                    "rarity": self.ModernWarfare.GetLootRarity(entry.get("quality")),
                    "season": self.ModernWarfare.GetLootSeason(entry.get("license")),
                    "challengeId": entry.get("ref"),
                    "image": entry.get("missionImage"),
                    "background": "ui_loot_bg_feature",
                    "rewards": [
                        {
                            "id": (lId := entry.get("operatorSkinID")),
                            "type": self.ModernWarfare.GetLootType(lId),
                        }
                    ],
                }
            )

        return items


class BRMissions:
    """BR Missions XAssets."""

    def Compile(self: Any) -> None:
        """Compile the BR Missions XAssets."""

        missions: List[Dict[str, Any]] = []

        missions = BRMissions.Table(self, missions)

        Utility.WriteFile(self, f"{self.eXAssets}/brMissions.json", missions)

        log.info(f"Compiled {len(missions):,} BR Missions")

    def Table(self: Any, missions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/brmissions.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/brmissions.csv", BRMissionsTable
        )

        if table is None:
            return missions

        for entry in table:
            title: Optional[str] = self.localize.get(entry.get("title"))

            if title is None:
                title = self.localize.get(entry.get("mapKeyTitle"))

            missions.append(
                {
                    "altId": entry.get("ref"),
                    "name": None if title is None else title.title(),
                    "description": self.localize.get(entry.get("description")),
                    "image": entry.get("icon"),
                    "timed": bool(entry.get("hasTimer")),
                }
            )

        return missions
