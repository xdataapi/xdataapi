"""LlamaIndex tool spec for xdataapi.io: read-only public X (Twitter) data.

Every method is a tool. The docstring is what the model reads, so each one says
what the call costs in credits.
"""

from __future__ import annotations

import functools
import re
from typing import Any, Callable, List, Optional
from urllib.parse import quote

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from .client import XdataapiAuthError, XdataapiClient, XdataapiError

__all__ = ["XdataapiToolSpec", "XdataapiClient", "XdataapiError", "XdataapiAuthError"]


def _bad_request(message: str) -> dict:
    """An argument error in the shape of an API error, so the model can repair the call."""
    return {"error": {"code": "bad_request", "message": message}}


_USER_ID = re.compile(r"^\d{1,19}$")


def _handle(value: str) -> str:
    return value.strip().lstrip("@")


class _BadArgument(ValueError):
    """An argument no request can be built from."""


def _seg(value: Any) -> str:
    """One URL path segment. The value comes from a model, so nothing in it may
    act as a path: a slash is sent percent-encoded, and a segment that is empty
    or only dots ("..") is refused, because encoding does not change a dot."""
    s = str(value).strip()
    if s.strip(".") == "":
        raise _BadArgument("a handle, user or id must not be empty or only dots")
    return quote(s, safe="")


def _repairable(fn: Callable[..., dict]) -> Callable[..., dict]:
    """Give a bad argument back as data, like an API error, so the model can repair the call."""

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> dict:
        try:
            return fn(*args, **kwargs)
        except _BadArgument as err:
            return _bad_request(str(err))

    return wrapper


class XdataapiToolSpec(BaseToolSpec):
    """Read public X (Twitter) data: profiles, posts, threads, followers, search.

    Read-only. No posting, no likes, no direct messages, no private data.

    Args:
        api_key: Key from https://xdataapi.io/dashboard. Read from
            ``XDATAAPI_KEY`` when not given.
        max_results: Ceiling on the page size of every paging tool, so one agent
            step cannot spend more than you allow.
    """

    spec_functions = [
        "search_tweets",
        "get_user",
        "get_users",
        "get_user_tweets",
        "get_tweet",
        "get_tweets",
        "get_thread",
        "get_replies",
        "get_quotes",
        "get_retweeters",
        "get_followers",
        "get_follower_ids",
        "get_following",
        "get_balance",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        max_results: Optional[int] = None,
        **client_kwargs: Any,
    ) -> None:
        self.client = XdataapiClient(api_key, max_results=max_results, **client_kwargs)

    # --- tweets ----------------------------------------------------------

    def search_tweets(
        self,
        q: str,
        product: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict:
        """Search public X posts with the x.com operators.

        The entry point when you do not already know a handle or a post id.
        Costs 1 credit per result; an empty result is free.

        Args:
            q: x.com search syntax. Operators: from:handle, to:handle,
                since:YYYY-MM-DD, until:YYYY-MM-DD, min_faves:N, lang:xx,
                "exact phrase", OR, and - to exclude.
                Example: from:vercel since:2026-09-01 -filter:replies
            product: Latest (default, always available), Top (may answer 403,
                free), People (returns profiles), Photos, Videos.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            "/v1/tweets/search",
            {"q": q, "product": product, "count": self.client.cap(count), "cursor": cursor},
        )

    @_repairable
    def get_tweet(self, id: str) -> dict:
        """Read one X post by numeric id, with its author. Costs 1 credit.

        Args:
            id: Numeric post id, as a string.
        """
        return self.client.get(f"/v1/tweets/{_seg(id)}")

    def get_tweets(self, ids: List[str]) -> dict:
        """Read up to 100 X posts by id in ONE call.

        Prefer this over repeated single reads: one request, one rate-limit slot.
        Costs 1 credit per post found; deleted or private posts are listed in
        ``errors`` and cost nothing.

        Args:
            ids: Numeric post ids, at most 100.
        """
        return self.client.get("/v1/tweets/batch", {"ids": ",".join(str(i) for i in ids)})

    @_repairable
    def get_thread(self, id: str, cursor: Optional[str] = None) -> dict:
        """Read one X post with its thread and replies, focal post first.

        Reads a whole conversation in one call. Costs 1 credit per post returned.

        Args:
            id: Numeric post id, as a string.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(f"/v1/tweets/{_seg(id)}/thread", {"cursor": cursor})

    @_repairable
    def get_replies(self, id: str, cursor: Optional[str] = None) -> dict:
        """Read the direct replies to one X post, one page. Costs 1 credit per reply.

        Args:
            id: Numeric post id, as a string.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(f"/v1/tweets/{_seg(id)}/replies", {"cursor": cursor})

    @_repairable
    def get_quotes(self, id: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the posts that quote one X post, newest first. Costs 1 credit per post.

        Args:
            id: Numeric post id, as a string.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/tweets/{_seg(id)}/quotes", {"count": self.client.cap(count), "cursor": cursor}
        )

    @_repairable
    def get_retweeters(self, id: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the accounts that reposted one X post. Costs 0.5 credit per profile.

        Some reading accounts are refused this by X; a 403 is free.

        Args:
            id: Numeric post id, as a string.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/tweets/{_seg(id)}/retweeters", {"count": self.client.cap(count), "cursor": cursor}
        )

    # --- users -----------------------------------------------------------

    @_repairable
    def get_user(self, handle: Optional[str] = None, id: Optional[str] = None) -> dict:
        """Read the public profile of one X user, by handle or by user id. Costs 1 credit.

        Give one of the two. The id stays the same when the user changes the handle.

        Args:
            handle: X handle, with or without the leading @.
            id: Numeric user id, in place of the handle.
        """
        if (handle is None) == (id is None):
            return _bad_request("give handle or id, one of the two")
        if id is not None:
            if not _USER_ID.match(str(id).strip()):
                return _bad_request("id must be a numeric user id")
            return self.client.get(f"/v1/users/id/{_seg(id)}")
        return self.client.get(f"/v1/users/{_seg(_handle(handle or ''))}")

    def get_users(self, handles: Optional[List[str]] = None, ids: Optional[List[str]] = None) -> dict:
        """Read up to 100 X profiles in ONE call, by handle or by user id.

        Give one of the two lists. Prefer this over repeated single reads. Costs 1
        credit per profile found; inputs that do not exist are listed in ``errors``
        and cost nothing.

        Args:
            handles: X handles, at most 100.
            ids: Numeric user ids, at most 100, in place of the handles.
        """
        if (handles is None) == (ids is None):
            return _bad_request("give handles or ids, one of the two")
        if ids is not None:
            clean = [str(i).strip() for i in ids]
            if not all(_USER_ID.match(i) for i in clean):
                return _bad_request("ids must be numeric user ids")
            return self.client.get("/v1/users/batch", {"ids": ",".join(clean)})
        return self.client.get("/v1/users/batch", {"handles": ",".join(_handle(h) for h in handles or [])})

    @_repairable
    def get_user_tweets(
        self, user: str, count: Optional[int] = None, cursor: Optional[str] = None
    ) -> dict:
        """Read the latest posts of one X user, newest first. Costs 1 credit per post.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_seg(_handle(user))}/tweets", {"count": self.client.cap(count), "cursor": cursor}
        )

    @_repairable
    def get_followers(self, user: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the followers of an X user as full profiles. Costs 0.1 credit per profile.

        Use get_follower_ids when ids are enough: it costs five times less.
        Some reading accounts are refused this by X; a 403 is free.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_seg(_handle(user))}/followers", {"count": self.client.cap(count), "cursor": cursor}
        )

    @_repairable
    def get_follower_ids(
        self, user: str, count: Optional[int] = None, cursor: Optional[str] = None
    ) -> dict:
        """Read the numeric ids of an X user's followers, without profiles.

        Costs 0.02 credit per id. Use it to size or intersect an audience.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_seg(_handle(user))}/followers/ids",
            {"count": self.client.cap(count), "cursor": cursor},
        )

    @_repairable
    def get_following(self, user: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the accounts an X user follows. Costs 0.1 credit per profile.

        Some reading accounts are refused this by X; a 403 is free.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_seg(_handle(user))}/following", {"count": self.client.cap(count), "cursor": cursor}
        )

    # --- account ---------------------------------------------------------

    def get_balance(self) -> dict:
        """Read the credits left on this key and its rate limit. Free.

        Call it before a large read to check the budget covers the plan.
        """
        return self.client.get("/v1/me")
