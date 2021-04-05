"""Test universal resolver with did-comm messaging."""


import os

import pytest
from aries_cloudagent.messaging.request_context import RequestContext
from aries_cloudagent.resolver.base import ResolverError
from asynctest import mock as async_mock

# import didcomm_resolver.protocol.v0_9 as test_module
from didcomm_resolver import DIDCommResolver

# pylint: disable=redefined-outer-name


@pytest.fixture
def resolver():
    """Resolver fixture."""
    uni_resolver = DIDCommResolver()
    uni_resolver.configure(
        {
            "endpoint": "https://dev.uniresolver.io/1.0/identifiers",
            "methods": [
                "sov",
                "abt",
                "btcr",
                "erc725",
                "dom",
                "stack",
                "ethr",
                "web",
                "v1",
                "key",
                "ipid",
                "jolo",
                "hacera",
                "elem",
                "seraphid",
                "github",
                "ccp",
                "work",
                "ont",
                "kilt",
                "evan",
                "echo",
                "factom",
                "dock",
                "trust",
                "io",
                "bba",
                "bid",
                "schema",
                "ion",
                "ace",
                "gatc",
                "unisot",
                "icon",
            ],
        }
    )
    yield uni_resolver


@pytest.fixture
def profile():
    """Profile fixture."""
    yield async_mock.MagicMock()


class MockResponse:
    """Mock didcomm response."""

    pass


class MockClientSession:
    """Mock client session."""

    def __init__(self, response: MockResponse = None):
        self.response = response

    def __call__(self):
        return self

    async def __aenter__(self):
        """For use as async context."""
        return self

    async def __aexit__(self, err_type, err_value, err_exc):
        """For use as async context."""

    def get(self, endpoint):
        """Return response."""
        return self.response


@pytest.fixture
def context():
    yield RequestContext.test_context()


FAKE_YAML0 = "endpoint: magic\rmethods: test"


@async_mock.patch(
    "builtins.open", new_callable=async_mock.mock_open, read_data=FAKE_YAML0
)
@pytest.mark.asyncio
async def test_setup(mock_open, resolver, context):
    with async_mock.patch.dict(os.environ, {"UNI_RESOLVER_CONFIG": "fake_config"}):
        await resolver.setup(context)
        assert resolver._supported_methods == "test"


@pytest.mark.asyncio
@async_mock.patch('os.environ')
async def test_setup_env_error(env_mock, resolver, context):
    env_mock.get.return_value = "error"
    with pytest.raises(ResolverError):
        await resolver.setup(context)


FAKE_YAML1 = "NO_endpoint: magic\rNo_methodZ: test"


@async_mock.patch(
    "builtins.open", new_callable=async_mock.mock_open, read_data=FAKE_YAML1
)
@pytest.mark.asyncio
async def test_setup_yaml_error(mock_open, resolver, context):
    with async_mock.patch.dict(os.environ, {"UNI_RESOLVER_CONFIG": "fake_config"}):
        with pytest.raises(ResolverError):
            await resolver.setup(context)


def test_supported_methods(resolver):
    assert resolver.supported_methods


def test_configre_error(resolver):
    with pytest.raises(ResolverError):
        resolver.configure({"fake": "configure"})
