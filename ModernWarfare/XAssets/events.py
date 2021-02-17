import logging
from typing import Any, Dict, List, Optional, TypedDict, Union

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)

class SeasonalEvent(TypedDict):
    """Structure of mp/seasonal_event.csv"""

    id: int
    eventID: int
    lootID: int
    challengeRef: str
    order: int
    isFinalReward: int # bool
    location: str
    locationString: str
    isIntroGift: int # bool
    isEarlyAccessGift: int # bool
    backendChallengeRef: str
    targetProgress: int

class SeasonalEvents:
    """Seasonal Event XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Seasonal Event XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = SeasonalEvents.Table(self, challenges)

        Utility.WriteFile(
            self, f"{self.eXAssets}/seasonalEvents.json", challenges
        )

        log.info(f"Compiled {len(challenges):,} Seasonal Events")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/seasonal_event.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/seasonal_event.csv", SeasonalEvent
        )

        if table is None:
            return challenges

        for entry in table:
            challenges.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("challengeRef"),
                    "description": self.localize.get(entry.get("locationString")),
                    "eventId": entry.get("eventID"),
                    "finalReward": bool(entry.get("isFinalReward")),
                    "introGift": bool(entry.get("isIntroGift")),
                    "earlyAccessGift": bool(entry.get("isEarlyAccessGift")),
                    "rewards": [{"id": (lId := entry.get("lootID")), "type": self.ModernWarfare.GetLootType(lId)}]
                }
            )

        return challenges
