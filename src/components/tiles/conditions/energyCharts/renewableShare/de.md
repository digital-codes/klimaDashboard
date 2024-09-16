## Anteil erneuerbarer Energie (Energy-Charts)

Electricity traffic signal

Returns the renewable share of load in percent from today until prediction is currently available and the corresponding traffic light.

The traffic light "signal" is indicated by the following numbers:

-1: Red (grid congestion),
0: Red (low renewable share),
1: Yellow (average renewable share),
2: Green (high renewable share)

If no data is available from the primary data providers, a best guess is made from historic data. This is indicated by "substitute" set to True.

"postal_code" is an optional input parameter, which will consider the local grid state (e.g. transmission line overload) in future implementations.

Response schema:

{
    "unix_seconds": [int],
    "share": [float],
    "signal": [int],
    "substitute": bool,
    "deprecated": bool
}
