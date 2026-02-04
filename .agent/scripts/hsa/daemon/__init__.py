# HSA v5.0 Daemon Module
# =============================================================================
"""
Daemon server and client for HSA v5.0.

Server:
    python -m hsa.daemon --host 127.0.0.1 --port 9527
    
Client:
    from hsa.daemon import HSAClient
    
    async with HSAClient() as client:
        await client.search("query")
"""

from .server import (
    HSADaemon,
    DaemonConfig,
    RequestHandler,
    Request,
    Response,
    run_daemon,
    main,
)

from .client import (
    HSAClient,
    SyncHSAClient,
    ClientConfig,
    connect,
    connect_sync,
)

__all__ = [
    # Server
    "HSADaemon",
    "DaemonConfig",
    "RequestHandler",
    "Request",
    "Response",
    "run_daemon",
    "main",
    # Client
    "HSAClient",
    "SyncHSAClient",
    "ClientConfig",
    "connect",
    "connect_sync",
]
