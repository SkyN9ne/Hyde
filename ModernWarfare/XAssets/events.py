import logging
from typing import Any, Dict, List, TypedDict, Union

from utility import Utility

log: logging.Logger = logging.getLogger(__name__)


class SeasonalEvent(TypedDict):
    """Structure of mp/seasonal_event.csv"""

    id: int
    eventID: int
    lootID: int
    challengeRef: str
    order: int
    isFinalReward: int  # bool
    location: str
    locationString: str
    isIntroGift: int  # bool
    isEarlyAccessGift: int  # bool
    backendChallengeRef: str
    targetProgress: int
    gameSource: str
    billboardImage: str
    challengeCompletedImage: str
    shortDesc: str


class BRPlaylistEvents(TypedDict):
    """Structure of mp/br_playlist_events.csv"""

    ref: int
    categoryName: str
    description: str
    disabledText: str
    background: str
    themeColorSwatch: str
    koreaDisabled: int  # bool


class SeasonalEvents:
    """Seasonal Event XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Seasonal Event XAssets."""

        challenges: List[Dict[str, Any]] = []

        challenges = SeasonalEvents.Table(self, challenges)

        Utility.WriteFile(self, f"{self.eXAssets}/seasonalEvents.json", challenges)

        log.info(f"Compiled {len(challenges):,} Seasonal Events")

    def Table(self: Any, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/seasonal_event.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/seasonal_event.csv", SeasonalEvent
        )

        if table is None:
            return challenges

        for entry in table:
            desc = self.localize.get(entry.get("locationString"))

            challenges.append(
                {
                    "id": entry.get("id"),
                    "altId": entry.get("challengeRef"),
                    "description": desc,
                    "altDescription": self.localize.get(entry.get("shortDesc")),
                    "image": entry.get("challengeCompletedImage"),
                    "billboard": entry.get("billboardImage"),
                    "eventId": entry.get("eventID"),
                    "finalReward": bool(entry.get("isFinalReward")),
                    "introGift": bool(entry.get("isIntroGift")),
                    "earlyAccessGift": bool(entry.get("isEarlyAccessGift")),
                    "gameSource": entry.get("gameSource"),
                    "rewards": [
                        {
                            "id": (lId := entry.get("lootID")),
                            "type": self.ModernWarfare.GetLootType(lId),
                        }
                    ],
                }
            )

            if desc is None:
                continue

            if (amount := entry.get("targetProgress")) is not None:
                challenges[-1]["description"] = desc.replace("&&1", f"{amount:,}")

        return challenges


class PlaylistEvents:
    """Playlist Event XAssets."""

    def Compile(self: Any) -> None:
        """Compile the Playlist Event XAssets."""

        events: List[Dict[str, Any]] = []

        events = PlaylistEvents.Table(self, events)

        Utility.WriteFile(self, f"{self.eXAssets}/playlistEvents.json", events)

        log.info(f"Compiled {len(events):,} Playlist Events")

    def Table(self: Any, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile the mp/br_playlist_events.csv XAsset."""

        table: List[Dict[str, Any]] = Utility.ReadCSV(
            self, f"{self.iXAssets}/mp/br_playlist_events.csv", BRPlaylistEvents, 1
        )

        if table is None:
            return events

        for entry in table:
            events.append(
                {
                    "name": self.localize.get(entry.get("categoryName")),
                    "description": self.localize.get(entry.get("description")),
                    "disabledText": self.localize.get(entry.get("disabledText")),
                    "colorSwatch": entry.get("themeColorSwatch"),
                    "image": entry.get("background"),
                }
            )

        return events
