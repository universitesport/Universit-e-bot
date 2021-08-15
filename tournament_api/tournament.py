from __future__ import annotations

import asyncio
import ast
import enum
import json
import time
from typing import List

import aiohttp
from dateutil import parser

api_key       = "WG_HRV51-Yi1wPjRvnMmBQT01dBoJ9DvVD5pD4hUlq0"
client_id     = "6d8e44da40bce24c11beb5de4i9qojcvtzswcwo8ko0og04cg8kw0ogs04gwgk0gcw88swg8c0"
client_secret = "53uihk4m9jgosckc00ss4gw8skowwwwo8so0kswksk8kg8k048"

class FromJSON:

    __slots__ = ()
    datetime = ()

    def __init__(self, data):
        for name in self.__slots__:
            if name in self.datetime:
                setattr(self, name, parser.parse(data.get(name)))
            else:
                setattr(self, name, data.get(name))


class Bracket(FromJSON): # no idea what this is used for

    __slots__ = (
        "id",
        "tournament_id",
        "stage_id",
        "group_id",
        "round_id",
        "number",
        "type",
        "status",
        "scheduled_datetime",
        "played_at",
        "depth",
        "branch",
        "opponents"
    )

    datetime = ("scheduled_datetime", "played_at")


class CustomField(FromJSON):

    __slots__ = (
        "label",
        "default_value",
        "required",
        "public",
        "position",
        "machine_name",
        "type",
        "target_type",
        "id",
        "tournament_id"
    )


class Discipline(FromJSON): # partial / full

    __slots__ = (
        "id",
        "name",
        "shortname",
        "fullname",
        "copyrights",

        "platforms_available",
        "team_size",
        "features"
    )


class StandingItem(FromJSON): # no idea what this is used for

    __slots__ = (
        "id",
        "position",
        "rank",
        "participant",
        "tournament_id"
    )


class Groups(FromJSON):

    __slots__ = (
        "id",
        "stage_id",
        "number",
        "name",
        "closed",
        "settings",
        "tournament_id"
    )


class Match(FromJSON):

    __slots__ = (
        "scheduled_datetime",
        "public_note",
        "private_note",
        "id",
        "status",
        "stage_id",
        "group_id",
        "round_id",
        "number",
        "type",
        "settings",
        "played_at",
        "report_closed",
        "opponents",
        "report_status",
        "tournament_id"
    )

    datetime = ("scheduled_datetime", "played_at")


class Game(FromJSON):

    __slots__ = (
        "status",
        "opponents",
        "number"
    )


class Report(FromJSON):

    __slots__ = (
        "note",
        "user_id",
        "custom_user_identifier",
        "report",
        "participant_id",
        "type",
        "id",
        "closed",
        "closed_at",
        "closed_author_id",
        "tournament_id",
        "match_id"
    )

    datetime = ("closed_at",)


class Tournament(FromJSON):

    __slots__ = (
        "name",
        "full_name",
        "scheduled_date_start",
        "scheduled_date_end",
        "timezone",
        "public",
        "size",
        "online",
        "location",
        "country",
        "logo",
        "registration_enabled",
        "registration_opening_datetime",
        "registration_closing_datetime",
        "organization",
        "contact",
        "discord",
        "website",
        "description",
        "rules",
        "prize",
        "match_report_enabled",
        "registration_request_message",
        "check_in_enabled",
        "check_in_participant_enabled",
        "check_in_participant_start_datetime",
        "check_in_participant_end_datetime",
        "archived",
        "registration_acceptance_message",
        "registration_refusal_message",
        "registration_terms_enabled",
        "registration_terms_url",
        "id",
        "discipline",
        "status",
        "participant_type",
        "platforms",
        "featured",
        "registration_notification_enabled",
        "team_min_size",
        "team_max_size"
    )

    datetime = ("scheduled_date_start", "scheduled_date_end", "registration_opening_datetime", "registration_closing_datetime")

    @property
    def videos(self):
        pass


class Participant(FromJSON):

    __slots__ = (
        "name",
        "email",
        "custom_user_identifier",
        "checked_in",
        "custom_fields",
        "id",
        "user_id",
        "created_at",
        "checked_in_at",
        "type",
        "tournament_id",
        "lineup"
    )


class Permission(FromJSON):

    __slots__ = (
        "attributes",
        "email",
        "id"
    )


class RankingItem(FromJSON):

    __slots__ = (
        "id",
        "group_id",
        "number",
        "position",
        "rank",
        "participant",
        "points",
        "properties",
        "tournament_id",
        "stage_id"
    )


class Registration(FromJSON):

    __slots__ = (
        "name",
        "email",
        "custom_user_identifier",
        "custom_fields",
        "id",
        "type",
        "tournament_id",
        "participant_id",
        "user_id",
        "status",
        "created_at",
        "lineup"
    )

    datetime = ("created_at",)


class Rounds(FromJSON):

    __slots__ = (
        "id",
        "stage_id",
        "group_id",
        "number",
        "name",
        "closed",
        "settings",
        "tournament_id"
    )


#Stages/Streams/video/webhook/webhook subscription


class Organizer(enum.Enum):

    view         = "view"
    admin        = "admin"
    result       = "result"
    participant  = "participant"
    registration = "registration"
    permission   = "permission"
    delete       = "delete"

    def __str__(self):
        return f"organizer:{self.value}"


class TokenManager:

    class Token:

        def __init__(self, emited=0, duration=0, key=None):
            self.emited = emited
            self.duration = duration
            self.key = key


    def __init__(self):
        self.token: Dict[Organizer, Token] = {value: TokenManager.Token() for value in Organizer}

    async def get_token(self, type):
        assert type in Organizer
        token = self.token[type]
        if token.emited + token.duration < time.time():
            headers = {"X-Api-Key": api_key}
            async with aiohttp.ClientSession(headers=headers) as session:

                data = {"grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "scope": str(type)}

                async with session.post("https://api.toornament.com/oauth/v2/token", data=data) as resp:
                    key = await resp.json()
                    self.token[type] = TokenManager.Token(time.time(), key["expires_in"], key["access_token"])
        return self.token[type].key


class Toornament:

    def __init__(self):
        self.token_manager = TokenManager()
        self.endpoint = "https://api.toornament.com/organizer/v2"

    async def get_tournament(self, id: int) -> Tournament:  # todo: factorize request getter

        headers = {"X-Api-Key": api_key,
                   "Authorization": await self.token_manager.get_token(Organizer.view)}

        async with aiohttp.ClientSession(headers=headers, raise_for_status=True) as session:
            async with session.get(f"{self.endpoint}/tournaments/{id}") as participant:
                result = await participant.json()
                return Tournament(result)


    async def get_participant(self, id: int) -> Participant:
        headers = {"X-Api-Key": api_key,
                   "Authorization": await self.token_manager.get_token(Organizer.participant)}

        async with aiohttp.ClientSession(headers=headers, raise_for_status=True) as session:
            async with session.get(f"https://api.toornament.com/organizer/v2/participants/{id}") as participant:
                result = await participant.json()
                return Participant(result)


try:
    test = Toornament()
    #t = asyncio.run(test.get_tournament(4835066204650110976))
    t = asyncio.run(test.get_participant(4855254197882290176))
    import pprint
    for a in t.__slots__:
         pprint.pprint(getattr(t, a))
except RuntimeError:
    pass
