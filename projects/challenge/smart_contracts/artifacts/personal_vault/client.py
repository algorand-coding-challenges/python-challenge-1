# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "deposit(pay)uint64": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "withdraw()uint64": {
            "call_config": {
                "close_out": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMucGVyc29uYWxfdmF1bHQuY29udHJhY3QuUGVyc29uYWxWYXVsdC5hcHByb3ZhbF9wcm9ncmFtOgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjE0CiAgICAvLyBjbGFzcyBQZXJzb25hbFZhdWx0KEFSQzRDb250cmFjdCk6CiAgICB0eG4gTnVtQXBwQXJncwogICAgYnogbWFpbl9iYXJlX3JvdXRpbmdANgogICAgbWV0aG9kICJkZXBvc2l0KHBheSl1aW50NjQiCiAgICBtZXRob2QgIndpdGhkcmF3KCl1aW50NjQiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBtYWluX2RlcG9zaXRfcm91dGVAMiBtYWluX3dpdGhkcmF3X3JvdXRlQDMKICAgIGVyciAvLyByZWplY3QgdHJhbnNhY3Rpb24KCm1haW5fZGVwb3NpdF9yb3V0ZUAyOgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjIyCiAgICAvLyBAYXJjNC5hYmltZXRob2QoKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBOb09wCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGlzIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjE0CiAgICAvLyBjbGFzcyBQZXJzb25hbFZhdWx0KEFSQzRDb250cmFjdCk6CiAgICB0eG4gR3JvdXBJbmRleAogICAgaW50IDEKICAgIC0KICAgIGR1cAogICAgZ3R4bnMgVHlwZUVudW0KICAgIGludCBwYXkKICAgID09CiAgICBhc3NlcnQgLy8gdHJhbnNhY3Rpb24gdHlwZSBpcyBwYXkKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToyMgogICAgLy8gQGFyYzQuYWJpbWV0aG9kKCkKICAgIGNhbGxzdWIgZGVwb3NpdAogICAgaXRvYgogICAgYnl0ZSAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50IDEKICAgIHJldHVybgoKbWFpbl93aXRoZHJhd19yb3V0ZUAzOgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjM4CiAgICAvLyBAYXJjNC5hYmltZXRob2QoYWxsb3dfYWN0aW9ucz1bIkNsb3NlT3V0Il0pCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBpbnQgQ2xvc2VPdXQKICAgID09CiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIENsb3NlT3V0CiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgYXNzZXJ0IC8vIGlzIG5vdCBjcmVhdGluZwogICAgY2FsbHN1YiB3aXRoZHJhdwogICAgaXRvYgogICAgYnl0ZSAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50IDEKICAgIHJldHVybgoKbWFpbl9iYXJlX3JvdXRpbmdANjoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToxNAogICAgLy8gY2xhc3MgUGVyc29uYWxWYXVsdChBUkM0Q29udHJhY3QpOgogICAgdHhuIE9uQ29tcGxldGlvbgogICAgc3dpdGNoIG1haW5fY3JlYXRlQDcgbWFpbl9vcHRfaW5fdG9fYXBwQDgKICAgIGVyciAvLyByZWplY3QgdHJhbnNhY3Rpb24KCm1haW5fY3JlYXRlQDc6CiAgICAvLyBzbWFydF9jb250cmFjdHMvcGVyc29uYWxfdmF1bHQvY29udHJhY3QucHk6MTQKICAgIC8vIGNsYXNzIFBlcnNvbmFsVmF1bHQoQVJDNENvbnRyYWN0KToKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICAhCiAgICBhc3NlcnQgLy8gaXMgY3JlYXRpbmcKICAgIGludCAxCiAgICByZXR1cm4KCm1haW5fb3B0X2luX3RvX2FwcEA4OgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjE4CiAgICAvLyBAYXJjNC5iYXJlbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJPcHRJbiJdKQogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBpcyBub3QgY3JlYXRpbmcKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToxOC0xOQogICAgLy8gQGFyYzQuYmFyZW1ldGhvZChhbGxvd19hY3Rpb25zPVsiT3B0SW4iXSkKICAgIC8vIGRlZiBvcHRfaW5fdG9fYXBwKHNlbGYpIC0+IE5vbmU6CiAgICBjYWxsc3ViIG9wdF9pbl90b19hcHAKICAgIGludCAxCiAgICByZXR1cm4KCgovLyBzbWFydF9jb250cmFjdHMucGVyc29uYWxfdmF1bHQuY29udHJhY3QuUGVyc29uYWxWYXVsdC5kZXBvc2l0KHB0eG46IHVpbnQ2NCkgLT4gdWludDY0OgpkZXBvc2l0OgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjIyLTIzCiAgICAvLyBAYXJjNC5hYmltZXRob2QoKQogICAgLy8gZGVmIGRlcG9zaXQoc2VsZiwgcHR4bjogZ3R4bi5QYXltZW50VHJhbnNhY3Rpb24pIC0+IFVJbnQ2NDoKICAgIHByb3RvIDEgMQogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjI0CiAgICAvLyBhc3NlcnQgcHR4bi5hbW91bnQgPiAwLCAiRGVwb3NpdCBhbW91bnQgbXVzdCBiZSBncmVhdGVyIHRoYW4gMCIKICAgIGZyYW1lX2RpZyAtMQogICAgZ3R4bnMgQW1vdW50CiAgICBkdXAKICAgIGFzc2VydCAvLyBEZXBvc2l0IGFtb3VudCBtdXN0IGJlIGdyZWF0ZXIgdGhhbiAwCiAgICAvLyBzbWFydF9jb250cmFjdHMvcGVyc29uYWxfdmF1bHQvY29udHJhY3QucHk6MjUtMjcKICAgIC8vICMgVGhpcyBjb21wYXJpc29uIGlzIHJlbW92ZWQgYmVjYXVzZSBpdCdzIG5vdCB2YWxpZCB0byBjb21wYXJlIGFuIElEIHdpdGggYW4gYWRkcmVzcyBkaXJlY3RseSBpbiB0aGUgY29udHJhY3QuCiAgICAvLyAjIGFzc2VydCAocHR4bi5yZWNlaXZlciA9PSBHbG9iYWwuY3VycmVudF9hcHBsaWNhdGlvbl9pZCksICJEZXBvc2l0IHJlY2VpdmVyIG11c3QgYmUgdGhlIGNvbnRyYWN0IGFkZHJlc3MiCiAgICAvLyBhc3NlcnQgcHR4bi5zZW5kZXIgPT0gVHhuLnNlbmRlciwgIkRlcG9zaXQgc2VuZGVyIG11c3QgYmUgdGhlIGNhbGxlciIKICAgIGZyYW1lX2RpZyAtMQogICAgZ3R4bnMgU2VuZGVyCiAgICB0eG4gU2VuZGVyCiAgICA9PQogICAgYXNzZXJ0IC8vIERlcG9zaXQgc2VuZGVyIG11c3QgYmUgdGhlIGNhbGxlcgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjI4LTMwCiAgICAvLyAjIFNpbmNlIHdlIGNhbid0IGRpcmVjdGx5IHZlcmlmeSB0aGUgY29udHJhY3QgYWRkcmVzcyBpbiB0aGUgY29udHJhY3QsIHdlIGVuc3VyZSB0aGUgc2VuZGVyIGhhcyBvcHRlZCBpbi4KICAgIC8vICMgTm90ZTogVGhlIHVzZSBvZiBHbG9iYWwuY3VycmVudF9hcHBsaWNhdGlvbl9hZGRyZXNzIGhlcmUgd2FzIGluY29ycmVjdCBkdWUgdG8gY29udGV4dDsgeW91IG1pZ2h0IG5lZWQgdG8gYWRqdXN0IHRoaXMgcGFydC4KICAgIC8vIGFzc2VydCBvcC5hcHBfb3B0ZWRfaW4oVHhuLnNlbmRlciwKICAgIHR4biBTZW5kZXIKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTozMQogICAgLy8gR2xvYmFsLmN1cnJlbnRfYXBwbGljYXRpb25faWQpLCAiRGVwb3NpdCBzZW5kZXIgbXVzdCBvcHQtaW4gdG8gdGhlIGFwcCBmaXJzdC4iCiAgICBnbG9iYWwgQ3VycmVudEFwcGxpY2F0aW9uSUQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToyOC0zMQogICAgLy8gIyBTaW5jZSB3ZSBjYW4ndCBkaXJlY3RseSB2ZXJpZnkgdGhlIGNvbnRyYWN0IGFkZHJlc3MgaW4gdGhlIGNvbnRyYWN0LCB3ZSBlbnN1cmUgdGhlIHNlbmRlciBoYXMgb3B0ZWQgaW4uCiAgICAvLyAjIE5vdGU6IFRoZSB1c2Ugb2YgR2xvYmFsLmN1cnJlbnRfYXBwbGljYXRpb25fYWRkcmVzcyBoZXJlIHdhcyBpbmNvcnJlY3QgZHVlIHRvIGNvbnRleHQ7IHlvdSBtaWdodCBuZWVkIHRvIGFkanVzdCB0aGlzIHBhcnQuCiAgICAvLyBhc3NlcnQgb3AuYXBwX29wdGVkX2luKFR4bi5zZW5kZXIsCiAgICAvLyAgICAgICAgICAgICAgICAgICAgICAgIEdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2lkKSwgIkRlcG9zaXQgc2VuZGVyIG11c3Qgb3B0LWluIHRvIHRoZSBhcHAgZmlyc3QuIgogICAgYXBwX29wdGVkX2luCiAgICBhc3NlcnQgLy8gRGVwb3NpdCBzZW5kZXIgbXVzdCBvcHQtaW4gdG8gdGhlIGFwcCBmaXJzdC4KICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTozMwogICAgLy8gc2VsZi5iYWxhbmNlW1R4bi5zZW5kZXJdICs9IHB0eG4uYW1vdW50CiAgICB0eG4gU2VuZGVyCiAgICBpbnQgMAogICAgYnl0ZSAiYmFsYW5jZSIKICAgIGFwcF9sb2NhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBiYWxhbmNlIGV4aXN0cyBmb3IgYWNjb3VudAogICAgKwogICAgdHhuIFNlbmRlcgogICAgYnl0ZSAiYmFsYW5jZSIKICAgIHVuY292ZXIgMgogICAgYXBwX2xvY2FsX3B1dAogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjM0CiAgICAvLyB1c2VyX2JhbGFuY2UgPSBzZWxmLmJhbGFuY2VbVHhuLnNlbmRlcl0KICAgIHR4biBTZW5kZXIKICAgIGludCAwCiAgICBieXRlICJiYWxhbmNlIgogICAgYXBwX2xvY2FsX2dldF9leAogICAgYXNzZXJ0IC8vIGNoZWNrIGJhbGFuY2UgZXhpc3RzIGZvciBhY2NvdW50CiAgICAvLyBzbWFydF9jb250cmFjdHMvcGVyc29uYWxfdmF1bHQvY29udHJhY3QucHk6MzYKICAgIC8vIHJldHVybiB1c2VyX2JhbGFuY2UKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5wZXJzb25hbF92YXVsdC5jb250cmFjdC5QZXJzb25hbFZhdWx0LndpdGhkcmF3KCkgLT4gdWludDY0Ogp3aXRoZHJhdzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTozOC0zOQogICAgLy8gQGFyYzQuYWJpbWV0aG9kKGFsbG93X2FjdGlvbnM9WyJDbG9zZU91dCJdKQogICAgLy8gZGVmIHdpdGhkcmF3KHNlbGYpIC0+IFVJbnQ2NDoKICAgIHByb3RvIDAgMQogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjQwCiAgICAvLyB1c2VyQmFsYW5jZSA9IHNlbGYuYmFsYW5jZVtUeG4uc2VuZGVyXQogICAgdHhuIFNlbmRlcgogICAgaW50IDAKICAgIGJ5dGUgImJhbGFuY2UiCiAgICBhcHBfbG9jYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgYmFsYW5jZSBleGlzdHMgZm9yIGFjY291bnQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTo0Mi00NwogICAgLy8gaXR4bi5QYXltZW50KAogICAgLy8gICAgIHJlY2VpdmVyPVR4bi5zZW5kZXIsCiAgICAvLyAgICAgc2VuZGVyPUdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2FkZHJlc3MsCiAgICAvLyAgICAgYW1vdW50PXVzZXJCYWxhbmNlLAogICAgLy8gICAgIGZlZT0wLAogICAgLy8gKS5zdWJtaXQoKQogICAgaXR4bl9iZWdpbgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjQzCiAgICAvLyByZWNlaXZlcj1UeG4uc2VuZGVyLAogICAgdHhuIFNlbmRlcgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjQ0CiAgICAvLyBzZW5kZXI9R2xvYmFsLmN1cnJlbnRfYXBwbGljYXRpb25fYWRkcmVzcywKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25BZGRyZXNzCiAgICAvLyBzbWFydF9jb250cmFjdHMvcGVyc29uYWxfdmF1bHQvY29udHJhY3QucHk6NDYKICAgIC8vIGZlZT0wLAogICAgaW50IDAKICAgIGl0eG5fZmllbGQgRmVlCiAgICBkaWcgMgogICAgaXR4bl9maWVsZCBBbW91bnQKICAgIGl0eG5fZmllbGQgU2VuZGVyCiAgICBpdHhuX2ZpZWxkIFJlY2VpdmVyCiAgICAvLyBzbWFydF9jb250cmFjdHMvcGVyc29uYWxfdmF1bHQvY29udHJhY3QucHk6NDIKICAgIC8vIGl0eG4uUGF5bWVudCgKICAgIGludCBwYXkKICAgIGl0eG5fZmllbGQgVHlwZUVudW0KICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTo0Mi00NwogICAgLy8gaXR4bi5QYXltZW50KAogICAgLy8gICAgIHJlY2VpdmVyPVR4bi5zZW5kZXIsCiAgICAvLyAgICAgc2VuZGVyPUdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2FkZHJlc3MsCiAgICAvLyAgICAgYW1vdW50PXVzZXJCYWxhbmNlLAogICAgLy8gICAgIGZlZT0wLAogICAgLy8gKS5zdWJtaXQoKQogICAgaXR4bl9zdWJtaXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weTo0OQogICAgLy8gcmV0dXJuIHVzZXJCYWxhbmNlCiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMucGVyc29uYWxfdmF1bHQuY29udHJhY3QuUGVyc29uYWxWYXVsdC5vcHRfaW5fdG9fYXBwKCkgLT4gdm9pZDoKb3B0X2luX3RvX2FwcDoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToxOC0xOQogICAgLy8gQGFyYzQuYmFyZW1ldGhvZChhbGxvd19hY3Rpb25zPVsiT3B0SW4iXSkKICAgIC8vIGRlZiBvcHRfaW5fdG9fYXBwKHNlbGYpIC0+IE5vbmU6CiAgICBwcm90byAwIDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9wZXJzb25hbF92YXVsdC9jb250cmFjdC5weToyMAogICAgLy8gc2VsZi5iYWxhbmNlW1R4bi5zZW5kZXJdID0gVUludDY0KDApCiAgICB0eG4gU2VuZGVyCiAgICBieXRlICJiYWxhbmNlIgogICAgaW50IDAKICAgIGFwcF9sb2NhbF9wdXQKICAgIHJldHN1Ygo=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMucGVyc29uYWxfdmF1bHQuY29udHJhY3QuUGVyc29uYWxWYXVsdC5jbGVhcl9zdGF0ZV9wcm9ncmFtOgogICAgLy8gc21hcnRfY29udHJhY3RzL3BlcnNvbmFsX3ZhdWx0L2NvbnRyYWN0LnB5OjE0CiAgICAvLyBjbGFzcyBQZXJzb25hbFZhdWx0KEFSQzRDb250cmFjdCk6CiAgICBpbnQgMQogICAgcmV0dXJuCg=="
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 1
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {
                "balance": {
                    "type": "uint64",
                    "key": "balance"
                }
            },
            "reserved": {}
        }
    },
    "contract": {
        "name": "PersonalVault",
        "methods": [
            {
                "name": "deposit",
                "args": [
                    {
                        "type": "pay",
                        "name": "ptxn"
                    }
                ],
                "returns": {
                    "type": "uint64"
                }
            },
            {
                "name": "withdraw",
                "args": [],
                "returns": {
                    "type": "uint64"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE",
        "opt_in": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data)
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class DepositArgs(_ArgsBase[int]):
    ptxn: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "deposit(pay)uint64"


@dataclasses.dataclass(kw_only=True)
class WithdrawArgs(_ArgsBase[int]):
    @staticmethod
    def method() -> str:
        return "withdraw()uint64"


class LocalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.balance = typing.cast(int, data.get(b"balance"))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def deposit(
        self,
        *,
        ptxn: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `deposit(pay)uint64` ABI method
        
        :param TransactionWithSigner ptxn: The `ptxn` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = DepositArgs(
            ptxn=ptxn,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_opt_in(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def close_out_withdraw(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `withdraw()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = WithdrawArgs()
        self.app_client.compose_close_out(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class PersonalVaultClient:
    """A class for interacting with the PersonalVault app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        PersonalVaultClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_local_state(self, account: str | None = None) -> LocalState:
        """Returns the application's local state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_local_state(account, raw=True))
        return LocalState(state)

    def deposit(
        self,
        *,
        ptxn: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[int]:
        """Calls `deposit(pay)uint64` ABI method
        
        :param TransactionWithSigner ptxn: The `ptxn` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[int]: The result of the transaction"""

        args = DepositArgs(
            ptxn=ptxn,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def opt_in_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the opt_in bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.opt_in(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def close_out_withdraw(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[int]:
        """Calls `withdraw()uint64` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[int]: The result of the transaction"""

        args = WithdrawArgs()
        result = self.app_client.close_out(
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
