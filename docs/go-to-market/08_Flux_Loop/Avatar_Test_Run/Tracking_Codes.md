# Tracking codes and links

Every video gets its own code, so each WhatsApp conversation can be traced
back to one video, for one business, in one format.

## The code

`AV` + two-digit business number + format letter.

| Example | Means |
|---|---|
| `AV00A` | FluxMuse (brand 0, the dry run), format A (avatar) |
| `AV03B` | Business 03, format B (product + voiceover) |
| `AV07C` | Business 07, format C (owner selfie) |

Business numbers come from the **Brands** tab of `Avatar_Test_Scoring.xlsx`.
00 is always FluxMuse.

Don't reuse FluxLoop's `FL-` prefix. The webhook reads `FL-` codes as ad
leads, and these aren't ads.

## The link

A `wa.me` link to the **business's own WhatsApp number**, with the code
pre-filled in the first message:

```
https://wa.me/<number, international, no + or spaces>?text=Hi%20<Business>!%20I%20saw%20your%20video%20(AV03B)
```

The **Tracking** tab builds the link and the caption line from the business
number and name, so you don't have to hand-type them.

**Caption line** (add at the end of the post): `Tap to chat: <link>`. If
links can't be tapped where it's posted (for example a Status image), use
**"WhatsApp us '<code>' to order"** instead.

## Counting conversations
- **Business uses FluxMuse for WhatsApp:** search Live Chat for the code.
  Each new conversation whose first message contains it counts once.
- **Business uses the WhatsApp Business app:** ask the owner to forward a
  screenshot of each chat that starts with the code, with the customer's name
  and number blurred. Count from those.
- **A customer messages without the code but says they saw the video:**
  count it, and note "no code" in the comments column.

## FluxMuse dry run (brand 0)
FluxMuse's own WhatsApp is **+27 74 242 6065**, where Fluxy answers.

| Code | Link |
|---|---|
| `AV00A` | `https://wa.me/27742426065?text=Hi%20FluxMuse!%20I%20saw%20your%20video%20(AV00A)` |
| `AV00B` | `https://wa.me/27742426065?text=Hi%20FluxMuse!%20I%20saw%20your%20video%20(AV00B)` |
| `AV00C` | `https://wa.me/27742426065?text=Hi%20FluxMuse!%20I%20saw%20your%20video%20(AV00C)` |

Fluxy will answer these chats. Read them in Live Chat, and step in if someone
asks something Fluxy can't handle.
