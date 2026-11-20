from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_users_tweets_body import GetUsersTweetsBody
from ...models.timeline_batch import TimelineBatch
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: GetUsersTweetsBody,
    fresh: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/users/tweets/batch",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TimelineBatch | None:
    if response.status_code == 200:
        response_200 = TimelineBatch.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Error | TimelineBatch]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersTweetsBody,
    fresh: bool | Unset = False,
) -> Response[Error | TimelineBatch]:
    """Latest tweets of many users, batch

     The newest tweets of up to 50 users in one call, by numeric user id: `count` tweets for each user (1
    to
    20, default 3). Newest first, retweets included, a pinned tweet in its place by date, as on
    `/v1/users/{user}/tweets`. 1 credit per tweet returned. A user with no public tweets is an entry
    with an
    empty `tweets` list and costs nothing; the profile (`/v1/users/batch`) tells you if the account is
    protected or suspended. A user that could not be read is in `errors` and costs nothing. Duplicates
    are
    folded. Results in input order.
    The `next_cursor` of an entry continues that timeline on `/v1/users/{user}/tweets`.
    Also `GET /v1/users/tweets/batch?ids=783214,813286&count=3`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.
    The limit counts `count` tweets for each user.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TimelineBatch]
    """

    kwargs = _get_kwargs(
        body=body,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersTweetsBody,
    fresh: bool | Unset = False,
) -> Error | TimelineBatch | None:
    """Latest tweets of many users, batch

     The newest tweets of up to 50 users in one call, by numeric user id: `count` tweets for each user (1
    to
    20, default 3). Newest first, retweets included, a pinned tweet in its place by date, as on
    `/v1/users/{user}/tweets`. 1 credit per tweet returned. A user with no public tweets is an entry
    with an
    empty `tweets` list and costs nothing; the profile (`/v1/users/batch`) tells you if the account is
    protected or suspended. A user that could not be read is in `errors` and costs nothing. Duplicates
    are
    folded. Results in input order.
    The `next_cursor` of an entry continues that timeline on `/v1/users/{user}/tweets`.
    Also `GET /v1/users/tweets/batch?ids=783214,813286&count=3`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.
    The limit counts `count` tweets for each user.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TimelineBatch
    """

    return sync_detailed(
        client=client,
        body=body,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersTweetsBody,
    fresh: bool | Unset = False,
) -> Response[Error | TimelineBatch]:
    """Latest tweets of many users, batch

     The newest tweets of up to 50 users in one call, by numeric user id: `count` tweets for each user (1
    to
    20, default 3). Newest first, retweets included, a pinned tweet in its place by date, as on
    `/v1/users/{user}/tweets`. 1 credit per tweet returned. A user with no public tweets is an entry
    with an
    empty `tweets` list and costs nothing; the profile (`/v1/users/batch`) tells you if the account is
    protected or suspended. A user that could not be read is in `errors` and costs nothing. Duplicates
    are
    folded. Results in input order.
    The `next_cursor` of an entry continues that timeline on `/v1/users/{user}/tweets`.
    Also `GET /v1/users/tweets/batch?ids=783214,813286&count=3`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.
    The limit counts `count` tweets for each user.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TimelineBatch]
    """

    kwargs = _get_kwargs(
        body=body,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersTweetsBody,
    fresh: bool | Unset = False,
) -> Error | TimelineBatch | None:
    """Latest tweets of many users, batch

     The newest tweets of up to 50 users in one call, by numeric user id: `count` tweets for each user (1
    to
    20, default 3). Newest first, retweets included, a pinned tweet in its place by date, as on
    `/v1/users/{user}/tweets`. 1 credit per tweet returned. A user with no public tweets is an entry
    with an
    empty `tweets` list and costs nothing; the profile (`/v1/users/batch`) tells you if the account is
    protected or suspended. A user that could not be read is in `errors` and costs nothing. Duplicates
    are
    folded. Results in input order.
    The `next_cursor` of an entry continues that timeline on `/v1/users/{user}/tweets`.
    Also `GET /v1/users/tweets/batch?ids=783214,813286&count=3`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.
    The limit counts `count` tweets for each user.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TimelineBatch
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            fresh=fresh,
        )
    ).parsed
